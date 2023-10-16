from typing import Any, List, Dict

import marshmallow as ma
from marshmallow import fields
from oarepo_model_builder.datatypes.containers.object import FieldSchema, ObjectDataType
from oarepo_model_builder.utils.python_name import convert_name_to_python
from oarepo_model_builder.validation import InvalidModelException
from oarepo_model_builder.validation.utils import ImportSchema

# model.setdefault("record-service-config-components", []).append(
#     "oarepo_runtime.relations.components.CachingRelationsComponent"
# )


class StringOrSchema(fields.Field):
    def __init__(self, string_field, schema_field, **kwargs) -> None:
        super().__init__(**kwargs)
        self.string_field = string_field
        self.schema_field = schema_field

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            return self.string_field._deserialize(value, attr, data, **kwargs)
        else:
            return self.schema_field._deserialize(value, attr, data, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, str):
            return self.string_field._serialize(value, attr, obj, **kwargs)
        else:
            return self.schema_field._serialize(value, attr, obj, **kwargs)

    def _validate(self, value):
        if isinstance(value, str):
            return self.string_field._validate(value)
        else:
            return self.schema_field._validate(value)


class RelationSchema(ma.Schema):
    class KeySchema(ma.Schema):
        key = fields.String(required=True)
        model = fields.Nested(FieldSchema, required=False)
        target = fields.String(required=False)

    name = fields.String(required=False)
    model = fields.String(required=True)
    keys_field = fields.List(
        StringOrSchema(ma.fields.String(), fields.Nested(KeySchema)),
        data_key="keys",
        attribute="keys",
        required=False,
    )
    class_ = fields.String(data_key="class", attribute="class", required=False)
    model_class = fields.String(
        data_key="model-class", attribute="model-class", required=False
    )
    related_part = fields.String(
        data_key="related-part", attribute="related-part", required=False
    )
    args = fields.Dict(
        fields.String(),
        fields.String(),
        required=False,
    )
    imports = fields.List(fields.Nested(ImportSchema), required=False)
    flatten = fields.Boolean(required=False)
    extras = fields.Raw(required=False)

    class Meta:
        unknown = ma.RAISE


class RelationDataType(ObjectDataType):
    model_type = "relation"
    flatten: bool
    model_name: str
    relation_name: str
    relation_class: str
    internal_link: bool
    relation_args: Dict[str, str]
    imports: List[Dict[str, str]]
    pid_field: str
    keys: List[Any]

    class ModelSchema(RelationSchema, ObjectDataType.ModelSchema):
        pass

    @property
    def relation(self):
        return {
            "name": self.relation_name,
            "relation_class": self.relation_class,
            "imports": self.imports,
            "path": self.path,
            "relation_args": self.relation_args,
        }

    def prepare(self, context):
        data = self.definition
        self.flatten = data.get("flatten", False)
        self.model_name = data["model"]
        self.internal_link = self.model_name.startswith("#")
        self.keys = self._transform_keys(
            data.get("keys", ["id", "metadata.title"]), self.flatten
        )
        self.relation_name = convert_name_to_python(data.get("name"))
        self.relation_class = data.get("class")
        self.imports = [*data.get("imports", [])]
        self.pid_field = data.get("pid-field")
        self.model_class = data.get("model-class")
        self.related_part = data.get("related-part")

        self.imports.append({"import": f"oarepo_runtime.relations.RelationsField"})

        if not self.relation_class:
            if self.internal_link:
                self.relation_class = "InternalRelation"
                self.imports.append(
                    {"import": f"oarepo_runtime.relations.InternalRelation"}
                )
            else:
                self.relation_class = "PIDRelation"
                self.imports.append({"import": f"oarepo_runtime.relations.PIDRelation"})

        self.relation_args = {**data.get("args", {})}

        written_keys = []
        for k in self.keys:
            if k["key"] == k["target"]:
                written_keys.append(k["key"])
            else:
                written_keys.append({"key": k["key"], "target": k["target"]})

        self.relation_args["keys"] = written_keys
        super().prepare(context)

    def _transform_keys(self, keys, flatten):
        transformed_keys = []
        for k in keys:
            if isinstance(k, str):
                k = {"key": k, "target": k}
            if not k.get("target"):
                k["target"] = k["key"]
            if flatten and k["target"].startswith("metadata."):
                k["target"] = k["target"][len("metadata.") :]
            transformed_keys.append(k)
        return transformed_keys


DATATYPES = [RelationDataType]
