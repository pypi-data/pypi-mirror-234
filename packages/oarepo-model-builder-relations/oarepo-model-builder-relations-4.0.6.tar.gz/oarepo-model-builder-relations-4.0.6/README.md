# Relations plugin for model builder

## Relation data type

The relation data type marks part of the metadata that will be filled with a related object.

Example usage - part of dataset model:

```yaml
primary-article:
    type:  relation
    name:  article
    model: article
    keys: ['metadata.title', 'metadata.authors']
```

The element "primary-article" will be connected to the article record. The record
class and properties will be taken from the "article" model
that is registered in "oarepo_models" entrypoint.

When returned to the user/serialized to ES, it will take the title and
author fields from the related model and copy them into the primary-article field.

It will automatically generate the following schema:

will generate:

```json5
// schema
{
    "primary-article": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "@v": {"type": "string"},
            "title": {},     // copied from registered article model
            "authors": {}    // copied from registered article model
        }
    }
}
```

```python
class Record:
    # ...
    relations = MultiRelationsField(
        article=PIDRelation(                # "name" from above
            "...primary-article",           # path inside the dataset model
            "keys": ['metadata.title', 'metadata.authors'],   # copied keys
            pid_field: Article.pid          # resolved model name and PID field
        )
    )
```

All arguments:

```yaml
primary-article:
    type: relation
    name: ...
    model: ...
    keys: [...]
    model-class:
    relation-classes:
        list: PIDListRelation
        nested: PIDNestedListRelation
        single: PIDRelation
    relation-class:
    relation-args:
        attrs: []
        keys: []
        _value_key_suffix: id
        _clear_empty: true
        cache_key:
        value_check:
        pid_field: model-class.pid
    imports:
    - import: invenio_records_resources.records.system_fields.relations.PIDRelation
      alias: PIDRelation
```


| Field            | Description   |
|------------------|---------------|
| name             | Relation name, will be used as param name inside RelationsField |
| model            | Name of the referenced model - from oarepo.models entrypoint or passed on commandline via --include parameter |
| keys             | Array of paths or dicts. If item is a path, that path will be copied from the referenced model. If it is dict it must contain the whole model definition. |
| model-class      | Class representing the related model |
| relation-classes | If the field is not an array and not nested inside an array, "single" is used. If the field is an array "list" is used. If the field is inside an array field, "nested" is used |
| relation-class   | can be used to override relation-classes |
| relation-args    | A dictionary of arguments that will be passes to the relation class |
| imports          | You can define your own imports/aliases here. The defaults are thise for list, nested and single relation classes |


## Internal relations

Sometimes it you might want to reference part of your document for indexing purposes etc. and not split the document into two records.
For these, internal relations can be used:

```yaml

properties:
    metadata:
        properties:
            obj{}:
                ^id: anchor-obj
                test: keyword
                id: keyword
```

On object/array item, define the "id" field containing your "symbolic" name of the target of the relation.
Then the definition of the relation will look like:

```yaml
properties:
    metadata:
        properties:
            internal-ref:
                type: relation
                model: "#anchor-obj"
                keys: [id, test]
```

## Supported relations

See [referrer.yaml](https://github.com/oarepo/oarepo-model-builder-relations/blob/main/tests/referrer.yaml) for a list of supported relations.