from bovine_store.utils.test import (  # noqa F401
    store,
    bovine_store_actor,
    bovine_admin_store,
)

from bovine_process.types import ProcessingItem

from .interactions import reply_handler


async def test_reply_handle_bare_object(store, bovine_store_actor):  # noqa F801
    remote_actor = "https://remote_domain/actor"
    first_id = "https://remote_domain/first"
    second_id = "https://remote_domain/second"
    create = {
        "@context": "about:bovine",
        "id": first_id,
        "type": "Create",
        "actor": remote_actor,
        "object": second_id,
    }

    processing_item = ProcessingItem(remote_actor, create)

    await reply_handler(processing_item, bovine_store_actor)
