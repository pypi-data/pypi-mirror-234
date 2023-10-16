import logging

from bovine_store.utils import add_sub_collections

from bovine_process.types import ProcessingItem

logger = logging.getLogger(__name__)


async def update_id(item: ProcessingItem, actor) -> ProcessingItem:
    """Assigns a new id to the object in data and possibly to the
    object in data["object"]"""
    data = await update_id_function(item.data, actor)
    item.data = data

    item.meta["object_location"] = data["id"]

    return item


async def update_id_function(data: dict, actor):
    data["id"] = actor.generate_new_object_id()
    if "object" in data and isinstance(data["object"], dict):
        if "id" in data["object"]:
            if data["object"]["id"] == actor.actor_id:
                return data

            obj_in_store = await actor.retrieve(data["object"]["id"])
            if not obj_in_store:
                data["object"]["id"] = actor.generate_new_object_id()
        else:
            data["object"]["id"] = actor.generate_new_object_id()

        data["object"] = add_sub_collections(data["object"])

    return data
