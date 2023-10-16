import logging

from bovine.parse import Activity
from bovine_process.types import ProcessingItem

logger = logging.getLogger(__name__)


async def accept_follow(item: ProcessingItem, actor) -> ProcessingItem:
    accept = Activity(item.data, domain=item.submitter_domain)
    follow = await accept.accept_for_follow(actor.retrieve)

    if follow and follow.actor_id == actor.actor_id:
        await actor.add_to_following(follow.object_id)
        logger.info(
            "Added %s to following %s", follow.object_id, actor.actor_object.following
        )

    return item


async def undo_follow(item: ProcessingItem, actor) -> ProcessingItem:
    undo = Activity(item.data, domain=item.submitter_domain)
    follow = await undo.undo_of_follow(actor.retrieve)

    if follow:
        await actor.remove_from_followers(follow.actor_id)
        logger.info(
            "Removed %s from followers %s",
            follow.actor_id,
            actor.actor_object.followers,
        )

    return item
