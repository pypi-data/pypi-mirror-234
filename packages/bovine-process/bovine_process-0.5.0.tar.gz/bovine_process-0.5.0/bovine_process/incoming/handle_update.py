import logging

from bovine.activitystreams.utils import actor_for_object

from bovine_process.types import ProcessingItem

logger = logging.getLogger(__name__)


async def handle_update(item: ProcessingItem, actor) -> ProcessingItem:
    owner = actor_for_object(item.data)

    object_to_update = item.data.get("object")
    if object_to_update is None or object_to_update.get("id") is None:
        logger.warning("Update without object %s", item.body)
        return

    to_update_from_db = await actor.retrieve_for(owner, object_to_update["id"])
    object_to_update["@context"] = item.data["@context"]

    if to_update_from_db:
        await actor.update_for(owner, object_to_update)

    return item
