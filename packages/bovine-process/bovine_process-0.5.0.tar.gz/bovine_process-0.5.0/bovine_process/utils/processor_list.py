import logging
import traceback

from .by_activity_type import ByActivityType

logger = logging.getLogger(__name__)


class ProcessorList:
    def __init__(self):
        self.processors = []

    def add(self, processor):
        self.processors.append(processor)
        return self

    def add_for_types(self, **kwargs):
        return self.add(ByActivityType(kwargs).act)

    async def apply(self, item, *arguments):
        working = item

        try:
            for processor in self.processors:
                working = await processor(working, *arguments)
                if not working:
                    return

            return working
        except Exception as ex:
            logger.warning(ex)
            for log_line in traceback.format_exc().splitlines():
                logger.error(log_line)
            raise ex
