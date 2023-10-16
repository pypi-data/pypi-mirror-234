from bovine_store.utils.test import (  # noqa F401
    store,
    bovine_store_actor,
    bovine_admin_store,
)


from bovine_process.types import ProcessingItem

from .outgoing_update import outgoing_update
from .store_outgoing import store_outgoing


async def test_basic_update(store, bovine_store_actor):  # noqa F801
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    third_id = "https://my_domain/third"
    create = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "actor": bovine_store_actor.actor_id,
        "object": {
            "type": "Note",
            "id": second_id,
            "content": "new",
            "attributedTo": bovine_store_actor.actor_id,
        },
    }

    update = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": third_id,
        "type": "Create",
        "actor": bovine_store_actor.actor_id,
        "object": {
            "type": "Note",
            "id": second_id,
            "content": "updated",
            "attributedTo": bovine_store_actor.actor_id,
        },
    }

    processing_item = ProcessingItem(bovine_store_actor.actor_id, create)

    await store_outgoing(processing_item, bovine_store_actor)

    stored = await store.retrieve(bovine_store_actor.actor_id, second_id)
    assert stored["content"] == "new"

    processing_item = ProcessingItem(bovine_store_actor.actor_id, update)
    await outgoing_update(processing_item, bovine_store_actor)

    stored = await store.retrieve(bovine_store_actor.actor_id, second_id)
    assert stored["content"] == "updated"
