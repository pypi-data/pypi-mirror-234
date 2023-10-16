import logging
import traceback

logger = logging.getLogger(__name__)


async def do_nothing(item, *args):
    return item


class ByActivityType:
    def __init__(self, actions: dict):
        self.actions = actions

    async def act(self, item, *args):
        try:
            item_type = item.data["type"]
            if item_type in self.actions:
                return await self.actions[item_type](item, *args)
            else:
                return item
        except Exception as ex:
            logger.error(f"Something went wrong with {ex} during procession")
            if item:
                logger.error(item.data)

            for log_line in traceback.format_exc().splitlines():
                logger.error(log_line)
