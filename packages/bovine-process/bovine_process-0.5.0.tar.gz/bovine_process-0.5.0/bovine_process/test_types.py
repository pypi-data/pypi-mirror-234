from .types import ProcessingItem


def test_get_object_id():
    def id_for_body(data):
        item = ProcessingItem("tag:author", data)
        return item.object_id()

    assert id_for_body({}).startswith("remote://")
    assert id_for_body({"id": "abc"}) == "abc"

    item = ProcessingItem("tag:author", {})

    assert item.object_id() == item.object_id()
