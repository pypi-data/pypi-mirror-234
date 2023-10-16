import pytest
from invenio_access.permissions import system_identity
from oarepo_runtime.relations.errors import InvalidRelationError
from referred.proxies import current_service as referred_service
from referrer.proxies import current_service as referrer_service


@pytest.fixture
def referred_record(app, db, search_clear):
    return referred_service.create(
        system_identity,
        {
            "metadata": {
                "title": "Referred Record",
                "description": "First referred record",
                "hint": "Just a random string",
                "price": 1,
            },
            "test": "cf",
        },
    )


@pytest.fixture
def referred_records(app, db, search_clear):
    return [
        referred_service.create(
            system_identity,
            {
                "metadata": {
                    "title": f"Referred Record # {idx}",
                    "description": f"Referred record # {idx} description",
                    "hint": f"Just a random string",
                    "price": idx,
                },
                "test": f"cf # {idx}",
            },
        )
        for idx in range(1, 11)
    ]


def test_invenio_relation(app, db, search_clear, referred_record):
    referrer_record = referrer_service.create(
        system_identity, {"metadata": {"invenio-ref": {"id": referred_record.id}}}
    )
    assert referrer_record.data["metadata"]["invenio-ref"]["id"] == referred_record.id
    assert (
        referrer_record.data["metadata"]["invenio-ref"]["metadata"]["title"]
        == referred_record.data["metadata"]["title"]
    )


def test_invenio_relation_with_extra_data(app, db, search_clear, referred_record):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "invenio-ref": {
                    "id": referred_record.id,
                    "extra-data": {"some extra": "data here"},
                }
            }
        },
    )
    assert referrer_record.data["metadata"]["invenio-ref"]["id"] == referred_record.id
    assert (
        referrer_record.data["metadata"]["invenio-ref"]["metadata"]["title"]
        == referred_record.data["metadata"]["title"]
    )


def test_invenio_list_relation(app, db, search_clear, referred_records):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "invenio-array": [
                    {"id": referred_record.id} for referred_record in referred_records
                ]
            }
        },
    )
    for i in range(len(referred_records)):
        assert (
            referrer_record.data["metadata"]["invenio-array"][i]["id"]
            == referred_records[i].id
        )
        assert (
            referrer_record.data["metadata"]["invenio-array"][i]["metadata"]["title"]
            == referred_records[i].data["metadata"]["title"]
        )


def test_invenio_nested_list_relation(app, db, search_clear, referred_records):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "invenio-nested": [
                    {"ref": {"id": referred_record.id}}
                    for referred_record in referred_records
                ]
            }
        },
    )
    for i in range(len(referred_records)):
        assert (
            referrer_record.data["metadata"]["invenio-nested"][i]["ref"]["id"]
            == referred_records[i].id
        )
        assert (
            referrer_record.data["metadata"]["invenio-nested"][i]["ref"]["metadata"][
                "title"
            ]
            == referred_records[i].data["metadata"]["title"]
        )


def test_metadata_relation(app, db, search_clear, referred_record):
    referrer_record = referrer_service.create(
        system_identity, {"metadata": {"ref": {"id": referred_record.id}}}
    )
    assert referrer_record.data["metadata"]["ref"]["id"] == referred_record.id
    assert (
        referrer_record.data["metadata"]["ref"]["title"]
        == referred_record.data["metadata"]["title"]
    )


def test_metadata_list_relation(app, db, search_clear, referred_records):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "array": [
                    {"id": referred_record.id} for referred_record in referred_records
                ]
            }
        },
    )
    for i in range(len(referred_records)):
        assert (
            referrer_record.data["metadata"]["array"][i]["id"] == referred_records[i].id
        )
        assert (
            referrer_record.data["metadata"]["array"][i]["title"]
            == referred_records[i].data["metadata"]["title"]
        )


def test_metadata_nested_list_relation(app, db, search_clear, referred_records):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "nested": [
                    {"ref": {"id": referred_record.id}}
                    for referred_record in referred_records
                ]
            }
        },
    )
    for i in range(len(referred_records)):
        assert (
            referrer_record.data["metadata"]["nested"][i]["ref"]["id"]
            == referred_records[i].id
        )
        assert (
            referrer_record.data["metadata"]["nested"][i]["ref"]["title"]
            == referred_records[i].data["metadata"]["title"]
        )


def test_invenio_nested_list_in_list_relation(app, db, search_clear, referred_records):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "invenio-array-nested": [
                    {"ref-arr": [{"id": referred_record.id}]}
                    for referred_record in referred_records
                ]
            }
        },
    )
    for i in range(len(referred_records)):
        assert (
            referrer_record.data["metadata"]["invenio-array-nested"][i]["ref-arr"][0][
                "id"
            ]
            == referred_records[i].id
        )
        assert (
            referrer_record.data["metadata"]["invenio-array-nested"][i]["ref-arr"][0][
                "metadata"
            ]["title"]
            == referred_records[i].data["metadata"]["title"]
        )


def test_metadata_nested_list_in_list_relation(app, db, search_clear, referred_records):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "array-nested": [
                    {"ref-arr": [{"id": referred_record.id}]}
                    for referred_record in referred_records
                ]
            }
        },
    )
    for i in range(len(referred_records)):
        assert (
            referrer_record.data["metadata"]["array-nested"][i]["ref-arr"][0]["id"]
            == referred_records[i].id
        )
        assert (
            referrer_record.data["metadata"]["array-nested"][i]["ref-arr"][0]["title"]
            == referred_records[i].data["metadata"]["title"]
        )


def test_custom_fields(app, db, search_clear, referred_record):
    referrer_record = referrer_service.create(
        system_identity, {"metadata": {"cf": {"id": referred_record.id}}}
    )
    assert referrer_record.data["metadata"]["cf"]["id"] == referred_record.id
    assert (
        referrer_record.data["metadata"]["cf"]["test"] == referred_record.data["test"]
    )


def test_invalid_reference(app, db, search_clear):
    try:
        referrer_record = referrer_service.create(
            system_identity, {"metadata": {"invenio-ref": {"id": "invalid_identifier"}}}
        )
        raise AssertionError("Should not get here")
    except InvalidRelationError as e:
        assert e.related_id == "invalid_identifier"
        assert e.location == "metadata.invenio-ref"
        assert "has not been found or there was an exception accessing it" in str(e)
