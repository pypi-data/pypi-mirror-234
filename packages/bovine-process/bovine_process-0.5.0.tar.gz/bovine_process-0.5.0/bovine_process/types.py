import json
import logging
import uuid
from dataclasses import dataclass, field
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


@dataclass
class ProcessingItem:
    """Represents an entity being processed"""

    submitter: str
    data: dict
    meta: dict = field(default_factory=dict)

    @property
    def submitter_domain(self):
        return urlparse(self.submitter).netloc

    def object_id(self):
        object_id = self.data.get("id")

        if object_id is None:
            object_id = f"remote://{str(uuid.uuid4())}"
            self.data["id"] = object_id

        return object_id

    def dump(self):
        logger.error(">>>> ITEM from %s <<<<", self.submitter)
        logger.error("data: %s", json.dumps(self.data))
        logger.error("meta: %s", json.dumps(self.meta))
        logger.error("   ")
