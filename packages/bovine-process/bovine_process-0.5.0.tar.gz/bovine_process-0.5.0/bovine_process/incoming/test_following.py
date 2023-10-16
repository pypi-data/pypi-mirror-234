from bovine_store.utils.test import (  # noqa F401
    store,
    bovine_store_actor,
    bovine_admin_store,
)


from bovine_process.types import ProcessingItem

from .following import accept_follow, undo_follow


async def test_accept_follow(store, bovine_store_actor):  # noqa F801
    remote_actor = "https://remote/actor"
    actor_object = bovine_store_actor.actor_object

    activity = {
        "@context": "about:bovine",
        "type": "Accept",
        "actor": remote_actor,
        "object": {
            "id": actor_object.id + "/follow",
            "actor": actor_object.id,
            "type": "Follow",
            "object": remote_actor,
        },
    }
    item = ProcessingItem(remote_actor, activity)

    await accept_follow(item, bovine_store_actor)

    following = await bovine_store_actor.resolve_endpoints({actor_object.following})

    assert remote_actor in following


async def test_undo_follow(store, bovine_store_actor):  # noqa F801
    remote_actor = "https://remote/actor"
    actor_object = bovine_store_actor.actor_object

    await bovine_store_actor.add_to_followers(remote_actor)

    activity = {
        "@context": "about:bovine",
        "type": "Undo",
        "actor": remote_actor,
        "object": {"actor": remote_actor, "type": "Follow", "object": actor_object.id},
    }
    item = ProcessingItem(remote_actor, activity)

    await undo_follow(item, bovine_store_actor)

    followers = await bovine_store_actor.resolve_endpoints({actor_object.followers})

    assert remote_actor not in followers
