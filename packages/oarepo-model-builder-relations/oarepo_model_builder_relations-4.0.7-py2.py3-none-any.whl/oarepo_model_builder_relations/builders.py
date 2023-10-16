from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder

from oarepo_model_builder_relations.datatypes import RelationDataType


class InvenioRecordRelationsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_relations"
    section = "record"
    template = "record_relations"

    def finish(self, **extra_kwargs):
        relations = []
        imports = {}
        for dt in self.current_model.deep_iter():
            if isinstance(dt, RelationDataType):
                rel = dt.section_relation.config
                relations.append(rel)
                for imp in rel.get('imports', []):
                    imports[(imp.get('import'), imp.get('alias'))] = imp

        if relations:
            super().finish(relations=relations, relation_imports=list(imports.values()))
