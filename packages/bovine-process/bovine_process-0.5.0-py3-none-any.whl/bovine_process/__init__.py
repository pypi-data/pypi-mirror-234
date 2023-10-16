import asyncio
import logging
import random

from bovine_store.actor.bovine_store_actor import BovineStoreActor

from .incoming import default_inbox_process
from .outgoing import default_async_outbox_process, default_outbox_process
from .send_item import send_outbox_item
from .types import ProcessingItem

logger = logging.getLogger(__name__)


async def process_inbox_item(
    item: ProcessingItem, actor: BovineStoreActor, retry=False
):
    """Asynchronous processing of an item arriving at the inbox"""

    try:
        logger.debug("Processing inbox request")
        result = await default_inbox_process(item, actor)
        return result
    except Exception:
        logger.error(">>>>> SOMETHING WENT WRONG IN PROCESSING <<<<<<")

        if item:
            item.dump()

        if not retry:
            wait_time = random.randint(3, 33)
            logger.error("Retrying in %d seconds", wait_time)
            await asyncio.sleep(wait_time)
            await process_inbox_item(item, actor, retry=True)


async def handle_outbox_item(
    item: ProcessingItem, actor: BovineStoreActor
) -> ProcessingItem | None:
    """Synchronous part of processing an outbox item. In particular
    it contains the logic to assign ids to the item"""

    return await default_outbox_process(item, actor)


async def process_outbox_item(item: ProcessingItem, actor: BovineStoreActor):
    """Asynchronous part of processing an outbox item. In particular
    it contains the logic of sending the message to all followers"""

    logger.debug("Processing outbox request")
    await default_async_outbox_process(item, actor)
    await send_outbox_item(item, actor)
