from bovine_store.utils.test import (  # noqa F401
    store,
    bovine_store_actor,
    bovine_admin_store,
)

from bovine_process.types import ProcessingItem

from .handle_update import handle_update
from .store_incoming import store_incoming


async def test_basic_update(store, bovine_store_actor):  # noqa F801
    remote_actor = "https://remote_domain/actor"
    first_id = "https://my_domain/first"
    second_id = "https://my_domain/second"
    third_id = "https://my_domain/third"
    create = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": first_id,
        "type": "Create",
        "actor": remote_actor,
        "object": {"type": "Note", "id": second_id, "content": "new"},
    }

    update = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": third_id,
        "type": "Create",
        "actor": remote_actor,
        "object": {"type": "Note", "id": second_id, "content": "updated"},
    }

    actor_id = bovine_store_actor.actor_object.id

    processing_item = ProcessingItem(remote_actor, create)

    await store_incoming(processing_item, bovine_store_actor)

    stored = await store.retrieve(actor_id, second_id)
    assert stored["content"] == "new"

    processing_item = ProcessingItem(remote_actor, update)
    await handle_update(processing_item, bovine_store_actor)

    stored = await store.retrieve(actor_id, second_id)
    assert stored["content"] == "updated"
