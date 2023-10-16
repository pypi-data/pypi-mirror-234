import logging

from bovine.activitystreams.utils import id_for_object
from bovine.parse import Activity
from bovine_process.types import ProcessingItem

logger = logging.getLogger(__name__)


async def like_handler(item: ProcessingItem, actor) -> ProcessingItem:
    """Adds object to the likes collection of the liked object, if

    * object being liked is owner by the receiving actor"""

    object_to_like = item.data.get("object")
    obj = await actor.retrieve_own_object(id_for_object(object_to_like))
    if obj:
        obj_id = id_for_object(obj)
        logger.info("Like Handler %s", obj_id)
        await actor.add_to_interaction("likes", obj_id, item.data.get("id"))

    return item


async def announce_handler(item: ProcessingItem, actor) -> ProcessingItem:
    """Adds object to the shares collection of the announced object, if

    * object being announced is owner by the receiving actor"""

    object_to_share = item.data.get("object")
    obj = await actor.retrieve_own_object(id_for_object(object_to_share))
    if obj:
        obj_id = id_for_object(obj)
        logger.info("Announce Handler %s", obj_id)
        await actor.add_to_interaction("shares", obj_id, item.data.get("id"))

    return item


async def reply_handler(item: ProcessingItem, actor) -> ProcessingItem:
    """Adds object to the replies collection. Object being replied to
    is determined from `inReplyTo`. Reply is added if the object
    belongs to the receiving actor."""
    create = Activity(item.data, domain=item.submitter_domain)
    remote = await create.object_for_create(actor.retrieve)

    if not remote:
        return item

    if not remote.in_reply_to:
        return item

    obj = await actor.retrieve_own_object(remote.in_reply_to)

    if obj:
        obj_id = id_for_object(obj)
        logger.info("Reply Handler %s", obj_id)
        await actor.add_to_interaction("replies", obj_id, remote.identifier)

    return item


async def delete_reply_handler(item: ProcessingItem, actor) -> ProcessingItem:
    """If a reply is deleted, removes it from the replies collection"""

    remote = item.data.get("object")
    if not remote:
        return item

    await actor.remove_references(remote)

    return item


async def undo_handler(item: ProcessingItem, actor) -> ProcessingItem:
    """For an Undo of a Like, Dislike, Announce , they are removed from
    the appropriate collection."""

    object_to_undo = id_for_object(item.data.get("object"))
    obj = await actor.retrieve(object_to_undo)
    if obj is None:
        return item
    remote_actor = id_for_object(item.data.get("actor"))
    if obj.get("actor") != remote_actor:
        logger.error("Mismatching actor in undo from %s", remote_actor)
        return

    obj_type = obj.get("type")
    if obj_type in ["Like", "Dislike", "http://litepub.social/ns#EmojiReact"]:
        logger.info("Undo Handler for Like of %s", obj.get("id"))
        await actor.remove_from_interaction("likes", obj.get("object"), obj.get("id"))
    elif obj_type == "Announce":
        logger.info("Undo Handler for Like of %s", obj.get("id"))
        await actor.remove_from_interaction("shares", obj.get("object"), obj.get("id"))

    return item
