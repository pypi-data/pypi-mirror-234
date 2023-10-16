import logging

from bovine.activitystreams.object_factory import Object
from bovine.activitystreams.utils import copy_to_and_cc

from bovine_process.types import ProcessingItem

logger = logging.getLogger(__name__)


async def outgoing_delete(item: ProcessingItem, actor) -> ProcessingItem:
    object_to_delete = item.data.get("object")

    if isinstance(object_to_delete, dict):
        object_to_delete = object_to_delete.get("id")

    if object_to_delete is None:
        logger.warning("Delete without object %s", item.body)
        return None

    to_update_from_db = await actor.retrieve(object_to_delete)

    tombstone = Object(type="Tombstone", id=object_to_delete).build()

    if to_update_from_db:
        await actor.update(tombstone)

    data = copy_to_and_cc(to_update_from_db, item.data)

    await actor.update(data)
    item.data = data

    return item
