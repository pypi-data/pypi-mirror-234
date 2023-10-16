import logging

from bovine.activitystreams.utils import is_public, recipients_for_object, remove_public

logger = logging.getLogger(__name__)


async def store_outgoing(item, actor):
    if is_public(item.data):
        await actor.store(item.data, as_public=True)
        logger.info("Owner %s, public", actor.actor_id)

    else:
        recipients = remove_public(recipients_for_object(item.data))
        recipients.add(actor.actor_id)

        await actor.store(item.data, visible_to=recipients)
        logger.info(
            "Owner %s Recipients %s", actor.actor_id, " | ".join(list(recipients))
        )

    return item


async def add_outgoing_to_outbox(item, actor):
    object_id = item.data.get("id")

    if object_id is None:
        logger.warning("Tried to store object with id to %s's outbox", actor.actor_id)
        return item

    stored_item = await actor.add_to_outbox(object_id)

    item.meta["database_id"] = stored_item.id

    return item
