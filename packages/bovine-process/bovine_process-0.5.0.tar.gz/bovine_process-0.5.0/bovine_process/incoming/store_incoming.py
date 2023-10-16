import logging

from bovine.activitystreams.utils import (
    actor_for_object,
    recipients_for_object,
    remove_public,
    is_public,
)

logger = logging.getLogger(__name__)


async def store_incoming(item, actor):
    owner = actor_for_object(item.data)
    public = is_public(item.data)
    if not public:
        recipients = remove_public(recipients_for_object(item.data))
        recipients.add(actor.actor_id)
        await actor.store_for(owner, item.data, visible_to=recipients)
        logger.info("Owner %s Recipients %s", owner, " | ".join(list(recipients)))
    else:
        await actor.store_for(owner, item.data, as_public=True)
        logger.info("Owner %s, public", owner)
    return item


async def add_incoming_to_inbox(item, actor):
    object_id = item.object_id()

    if object_id is None:
        logger.warning(
            "Tried to store object without id to inbox of %s", actor.actor_id
        )
        return item.data

    stored_item = await actor.add_to_inbox(object_id)

    item.meta["database_id"] = stored_item.id

    return item
