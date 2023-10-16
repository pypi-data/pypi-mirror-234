import logging

from bovine.activitystreams.object_factory import Object
from bovine.activitystreams.utils import actor_for_object
from bovine.jsonld import with_bovine_context
from bovine_process.types import ProcessingItem

logger = logging.getLogger(__name__)


async def incoming_delete(item: ProcessingItem, actor) -> ProcessingItem:
    owner = actor_for_object(item.data)
    object_to_delete = item.data.get("object")

    if isinstance(object_to_delete, dict):
        object_to_delete = object_to_delete.get("id")

    if object_to_delete is None:
        logger.warning("Delete without object %s", item.body)
        return

    to_update_from_db = await actor.retrieve_for(owner, object_to_delete)

    tombstone = with_bovine_context(
        Object(type="Tombstone", id=object_to_delete).build()
    )

    if to_update_from_db:
        await actor.update_for(owner, tombstone)

    return item
    # return None
