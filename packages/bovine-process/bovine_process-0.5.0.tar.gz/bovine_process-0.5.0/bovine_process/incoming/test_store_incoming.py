from bovine_store.utils.test import (  # noqa F401
    store,
    bovine_store_actor,
    bovine_admin_store,
)


from bovine_process.types import ProcessingItem

from .store_incoming import store_incoming


async def test_store_incoming(store, bovine_store_actor):  # noqa F801
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    item = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "object": {
            "type": "Note",
            "id": second_id,
        },
    }

    actor_id = bovine_store_actor.actor_object.id

    processing_item = ProcessingItem("tag:actor", item)

    result = await store_incoming(processing_item, bovine_store_actor)

    assert result == processing_item

    first = await store.retrieve(actor_id, first_id)
    second = await store.retrieve(actor_id, second_id)

    assert first["id"] == first_id
    assert first["object"] == second_id
    assert second["id"] == second_id
