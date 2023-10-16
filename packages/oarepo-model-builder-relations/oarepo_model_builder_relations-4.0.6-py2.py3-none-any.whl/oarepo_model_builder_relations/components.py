import json

from oarepo_model_builder.datatypes import (
    DataType,
    DataTypeComponent,
    ModelDataType,
    datatypes,
    ObjectDataType,
)
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.utils.python_name import convert_name_to_python, base_name
from oarepo_model_builder.validation import InvalidModelException

from oarepo_model_builder_relations.datatypes import RelationDataType
from oarepo_model_builder.utils.deepmerge import deepmerge


class RelationModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    affects = [DefaultsModelComponent]

    def after_model_prepare(self, datatype: DataType, *, context, **kwargs):
        relation_datatypes = []
        for dt in datatype.deep_iter():
            if isinstance(dt, RelationDataType):
                relation_datatypes.append(dt)

        for dt in relation_datatypes:
            datatypes.call_components(dt, "resolve_relation", context=context)
            datatypes.call_components(dt, "prepare_relation_children", context=context)
            datatypes.call_components(dt, "set_permissive_marshmallow", context=context)

        relation_names = {}
        for dt in relation_datatypes:
            datatypes.call_components(
                dt, "get_declared_relation_names", relation_names=relation_names
            )
        for dt in relation_datatypes:
            datatypes.call_components(
                dt, "set_relation_names", relation_names=relation_names
            )
        for dt in relation_datatypes:
            datatypes.call_components(dt, "set_relation_arguments")


class RelationComponent(DataTypeComponent):
    eligible_datatypes = [RelationDataType]

    def resolve_relation(self, datatype: RelationDataType, *, context, **kwargs):
        if datatype.internal_link:
            root_datatype = datatype.stack[0]
            dt_id = datatype.model_name[1:]
        else:
            loaded_schema = datatype.schema._load(datatype.model_name)
            root_datatype = datatypes.get_datatype(
                datatype, loaded_schema["model"], None, datatype.model, datatype.schema
            )
            root_datatype.prepare(
                {
                    "profile": context["profile"],
                    "profile_module": context["profile_module"],
                    "profile_upper": context["profile_upper"],
                }
            )
            if "#" in datatype.model_name:
                dt_id = datatype.model_name.split("#", maxsplit=1)[1]
            else:
                dt_id = None

        if not dt_id:
            datatype.related_data_type = root_datatype
            return

        for dt in root_datatype.deep_iter():
            if dt.id == dt_id:
                datatype.related_data_type = dt
                return

        raise InvalidModelException(
            f"No element found for reference {datatype.model_name}"
        )

    def prepare_relation_children(
        self, datatype: RelationDataType, *, context, **kwargs
    ):
        # insert properties
        children = {}
        child_tree = {}
        for fld in datatype.keys:
            if fld.get("model"):
                if "." in fld["target"]:
                    raise InvalidModelException(
                        "Can not reference relation with explicit schema to nested target location"
                    )
                child = datatypes.get_datatype(
                    datatype,
                    fld["model"],
                    fld["target"],
                    datatype.model,
                    datatype.schema,
                )
                child.prepare(context)
                child_tree[fld["target"]] = child
            else:
                child = self.find_child(
                    datatype.related_data_type,
                    fld,
                    child_tree,
                    datatype.flatten,
                    datatype.definition.get("extras", {}),
                )
            children[child.key] = child

        children["@v"] = datatypes.get_datatype(
            datatype,
            {
                "type": "keyword",
                "marshmallow": {
                    "field-name": "_version",
                    "field-class": "ma.fields.String",
                },
                "ui": {
                    "marshmallow": {
                        "field-name": "_version",
                        "field-class": "ma.fields.String",
                    }
                },
            },
            "@v",
            datatype.model,
            datatype.schema,
        )
        children["@v"].prepare(
            {
                "profile": context["profile"],
                "profile_module": context["profile_module"],
                "profile_upper": context["profile_upper"],
            }
        )

        datatype.children = children

    def set_permissive_marshmallow(
        self, datatype: RelationDataType, *, context, **kwargs
    ):
        marshmallow = datatype.definition.setdefault("marshmallow", {})
        marshmallow.setdefault("unknown", "INCLUDE")

        ui_marshmallow = datatype.definition.setdefault("ui", {}).setdefault(
            "marshmallow", {}
        )
        ui_marshmallow.setdefault("unknown", "INCLUDE")

    def find_child(self, datatype, fld, child_tree, flatten, datatype_properties):
        target = fld["key"].split(".")
        flatten = fld.get("flatten", flatten)
        dt = datatype
        stack = []
        for tidx, t in enumerate(target):
            while hasattr(dt, "item"):
                dt = dt.item
                if tidx > 0:
                    stack.append((None, dt, len(target) - tidx - 1 + 0.5))

            if t not in dt.children:
                raise InvalidModelException(
                    f"Path {target} not found in datatype "
                    f"{datatype.path}. "
                    f"Error at {dt.path}: {t} not found at its children. "
                    f"Datatype content:"
                    f"{json.dumps(datatype.definition, indent=4)}"
                )
            dt = dt.children[t]
            stack.append((t, dt, len(target) - tidx - 1))
        if flatten:
            ret = dt.copy()
            ret.key = fld["target"].rsplit(".", maxsplit=1)[-1]
            self.fix_marshmallow(ret)
        else:
            top_key, top_dt, top_level = stack[0]
            if top_key not in child_tree:
                top_dt = top_dt.copy(without_children=True)
                child_tree[top_key] = top_dt
                self.fix_marshmallow(top_dt)
            else:
                top_dt = child_tree[top_key]

            ret = top_dt
            for stack_key, stack_dt, stack_level in stack[1:]:
                if stack_key in top_dt.children:
                    top_dt = top_dt.children[stack_key]
                    continue
                if not stack_key:
                    if top_dt.item:
                        continue
                if stack_level:
                    created = dt.copy(without_children=True)
                else:
                    created = dt.copy()

                self.fix_marshmallow(created)
                if not ret:
                    ret = created
                if stack_key:
                    # add created to object
                    top_dt.children[stack_key] = created
                else:
                    # add created to array
                    top_dt.item = created

        if ret.key in datatype_properties:
            ret = ret.copy()
            deepmerge(ret.definition, datatype_properties[ret.key])

        return ret

    def fix_marshmallow(self, dt):
        def fix(base):
            # nothing to fix if there is no marshmallow section
            if "marshmallow" not in base:
                return
            marshmallow = {**base["marshmallow"]}
            base["marshmallow"] = marshmallow
            if marshmallow.get("read") is False:
                marshmallow.pop("read")
            if marshmallow.get("write") is False:
                marshmallow.pop("write")

            # if not generating the class, nothing to fix
            if marshmallow.get("generate", None) is False:
                return
            if "class" not in marshmallow:
                return
            # duplicate the marshmallow section so that we do not modify the referenced definition
            marshmallow["class"] = marshmallow["class"].rsplit(".", maxsplit=1)[-1]
            marshmallow.pop("module", None)

        fix(dt.definition)
        if "ui" in dt.definition:
            # duplicate ui section as well so that we do not modify the referenced definition
            dt.definition["ui"] = {
                **dt.definition["ui"],
            }
            fix(dt.definition["ui"])

    def get_declared_relation_names(self, datatype, *, relation_names, **kwargs):
        if datatype.relation_name and datatype.relation_name not in relation_names:
            relation_names[datatype.relation_name] = datatype

    def set_relation_names(self, datatype, *, relation_names, **kwargs):
        if (
            datatype.relation_name
            and relation_names[datatype.relation_name] is datatype
        ):
            return
        # conflict found, try to resolve it
        relation_name = datatype.relation_name
        p: DataType
        for p in reversed(datatype.stack):
            if p.key:
                if relation_name:
                    relation_name = convert_name_to_python(f"{p.key}_{relation_name}")
                else:
                    relation_name = convert_name_to_python(p.key)
                if relation_name not in relation_names:
                    # found unused name, use it
                    datatype.relation_name = relation_name
                    relation_names[relation_name] = datatype
                    return
        # could not get unused name, add _1, ... to it
        for p in range(1, 100):
            new_relation_name = f"{relation_name}_{p}"
            if new_relation_name not in relation_names:
                # found unused name, use it
                datatype.relation_name = new_relation_name
                relation_names[new_relation_name] = datatype
                return
        raise InvalidModelException(
            "Could not generate relation name for {datatype.path}: "
            'please specify "name" yourself.'
        )

    def set_relation_arguments(self, datatype, **kwargs):
        if datatype.internal_link:
            if not datatype.related_part:
                if datatype.related_data_type:
                    datatype.related_part = datatype.related_data_type.path
            if datatype.related_part:
                datatype.relation_args.setdefault(
                    "related_part", repr(datatype.related_part)
                )
        else:
            if not datatype.pid_field and not datatype.model_class:
                model_class = datatype.related_data_type.definition.get(
                    "record", {}
                ).get("class")
                datatype.model_class = base_name(model_class)
                datatype.imports.append({"import": model_class})
            if datatype.pid_field or datatype.model_class:
                datatype.relation_args.setdefault(
                    "pid_field", datatype.pid_field or f"{datatype.model_class}.pid"
                )
            else:
                raise InvalidModelException(
                    f"Either pid-field or model-class must be set at {self.path}"
                )


COMPONENTS = [RelationComponent, RelationModelComponent]
