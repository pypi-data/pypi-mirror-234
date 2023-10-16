import logging

from urllib.parse import urlparse
from bovine.parse import Activity
from bovine_process.types import ProcessingItem

logger = logging.getLogger(__name__)


async def accept_follow(item: ProcessingItem, actor) -> ProcessingItem:
    accept = Activity(item.data, domain=urlparse(item.submitter).netloc)
    follow = await accept.accept_for_follow(actor.retrieve)

    if follow and follow.object_id == actor.actor_id:
        await actor.add_to_followers(follow.actor_id)
        logger.info(
            "Added %s to followers %s", follow.actor_id, actor.actor_object.followers
        )

    return item


async def undo_follow(item: ProcessingItem, actor) -> ProcessingItem:
    if item.data["type"] != "Undo":
        return item

    obj = item.data["object"]
    if isinstance(obj, str):
        obj = await actor.retrieve(obj)

    if obj["type"] != "Follow":
        return item

    remote_actor = obj.get("object")

    await actor.remove_from_following(remote_actor)

    logger.info(
        "Removed %s from following %s", remote_actor, actor.actor_object.following
    )

    return item
