import pytest
from invenio_access.permissions import system_identity
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


def test_internal_relation(app, db, search_clear):
    referrer_record = referrer_service.create(
        system_identity,
        {"metadata": {"obj": {"id": "1", "test": "blah"}, "internal-ref": {"id": "1"}}},
    )
    assert (
        referrer_record.data["metadata"]["internal-ref"]["id"]
        == referrer_record.data["metadata"]["obj"]["id"]
    )
    assert (
        referrer_record.data["metadata"]["internal-ref"]["test"]
        == referrer_record.data["metadata"]["obj"]["test"]
    )


def test_internal_list_relation(app, db, search_clear):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "arr": [{"id": "1", "test": "blah"}],
                "internal-ref-arr": {"id": "1"},
            }
        },
    )
    assert (
        referrer_record.data["metadata"]["internal-ref-arr"]["id"]
        == referrer_record.data["metadata"]["arr"][0]["id"]
    )
    assert (
        referrer_record.data["metadata"]["internal-ref-arr"]["test"]
        == referrer_record.data["metadata"]["arr"][0]["test"]
    )


def test_internal_listobj_relation(app, db, search_clear):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "arrobj": [{"id": "1", "test": "blah"}],
                "internal-ref-arrobj": {"id": "1"},
            }
        },
    )
    assert (
        referrer_record.data["metadata"]["internal-ref-arrobj"]["id"]
        == referrer_record.data["metadata"]["arrobj"][0]["id"]
    )
    assert (
        referrer_record.data["metadata"]["internal-ref-arrobj"]["test"]
        == referrer_record.data["metadata"]["arrobj"][0]["test"]
    )


def test_internal_array_to_array_relation(app, db, search_clear):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "arr": [
                    {"id": "1", "test": "blah"},
                    {"id": "2", "test": "abc"},
                ],
                "internal-array-ref-array": [{"id": "1"}, {"id": "2"}],
            }
        },
    )
    assert (
        referrer_record.data["metadata"]["internal-array-ref-array"][0]["id"]
        == referrer_record.data["metadata"]["arr"][0]["id"]
    )
    assert (
        referrer_record.data["metadata"]["internal-array-ref-array"][0]["test"]
        == referrer_record.data["metadata"]["arr"][0]["test"]
    )
    assert (
        referrer_record.data["metadata"]["internal-array-ref-array"][1]["id"]
        == referrer_record.data["metadata"]["arr"][1]["id"]
    )
    assert (
        referrer_record.data["metadata"]["internal-array-ref-array"][1]["test"]
        == referrer_record.data["metadata"]["arr"][1]["test"]
    )


def test_internal_array_object_to_array_relation(app, db, search_clear):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "arr": [
                    {"id": "1", "test": "blah"},
                    {"id": "2", "test": "abc"},
                ],
                "internal-array-object-ref-array": [
                    {"ref": {"id": "1"}},
                    {"ref": {"id": "2"}},
                ],
            }
        },
    )
    assert (
        referrer_record.data["metadata"]["internal-array-object-ref-array"][0]["ref"][
            "id"
        ]
        == referrer_record.data["metadata"]["arr"][0]["id"]
    )
    assert (
        referrer_record.data["metadata"]["internal-array-object-ref-array"][0]["ref"][
            "test"
        ]
        == referrer_record.data["metadata"]["arr"][0]["test"]
    )
    assert (
        referrer_record.data["metadata"]["internal-array-object-ref-array"][1]["ref"][
            "id"
        ]
        == referrer_record.data["metadata"]["arr"][1]["id"]
    )
    assert (
        referrer_record.data["metadata"]["internal-array-object-ref-array"][1]["ref"][
            "test"
        ]
        == referrer_record.data["metadata"]["arr"][1]["test"]
    )


def test_internal_array_nested_relation(app, db, search_clear):
    referrer_record = referrer_service.create(
        system_identity,
        {
            "metadata": {
                "arr": [
                    {"id": "1", "test": "blah"},
                    {"id": "2", "test": "abc"},
                ],
                "internal-array-nested": [
                    {"ref-arr": [{"id": "1"}]},
                    {"ref-arr": [{"id": "2"}]},
                ],
            }
        },
    )
    assert (
        referrer_record.data["metadata"]["internal-array-nested"][0]["ref-arr"][0]["id"]
        == referrer_record.data["metadata"]["arr"][0]["id"]
    )
    assert (
        referrer_record.data["metadata"]["internal-array-nested"][0]["ref-arr"][0][
            "test"
        ]
        == referrer_record.data["metadata"]["arr"][0]["test"]
    )
    assert (
        referrer_record.data["metadata"]["internal-array-nested"][1]["ref-arr"][0]["id"]
        == referrer_record.data["metadata"]["arr"][1]["id"]
    )
    assert (
        referrer_record.data["metadata"]["internal-array-nested"][1]["ref-arr"][0][
            "test"
        ]
        == referrer_record.data["metadata"]["arr"][1]["test"]
    )


def test_custom_fields(app, db, search_clear):
    referrer_record = referrer_service.create(
        system_identity,
        {"metadata": {"internal-cf": {"id": ""}}, "test": "blah"},
    )
    assert (
        referrer_record.data["metadata"]["internal-cf"]["test"]
        == referrer_record.data["test"]
    )
