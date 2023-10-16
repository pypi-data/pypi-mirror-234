import logging

from bovine.jsonld import with_bovine_context

from bovine_process.utils.processor_list import ProcessorList

from .following import accept_follow, undo_follow
from .handle_update import handle_update
from .incoming_delete import incoming_delete
from .interactions import (
    announce_handler,
    delete_reply_handler,
    like_handler,
    reply_handler,
    undo_handler,
)
from .store_incoming import add_incoming_to_inbox, store_incoming

logger = logging.getLogger(__name__)


async def sanitize(item, actor):
    item.data = with_bovine_context(item.data)

    if item.submitter != item.data["actor"]:
        logger.error("Got wrong submitter for an activity %s", item.submitter)
        logger.error(item.data)
        # return

    return item


interaction_handlers = {
    **dict(
        Announce=announce_handler,
        Create=reply_handler,
        Delete=delete_reply_handler,
        Dislike=like_handler,
        Like=like_handler,
        Undo=undo_handler,
    ),
    "http://litepub.social/ns#EmojiReact": like_handler,
}
"""The handlers being called for interactions"""

crud_handlers = dict(Update=handle_update, Delete=incoming_delete)
"""The handlers being called for CRUD operations"""

social_handlers = dict(Accept=accept_follow, Undo=undo_follow)
"""The handlers being called for social interactions, i.e. updating the social graph

FIXME: Missing undo_follow ... and the other nonsense, I need somebody to draw me
a state machine for"""


default_inbox_process = (
    ProcessorList()
    .add(sanitize)
    .add(store_incoming)
    .add(add_incoming_to_inbox)
    .add_for_types(**crud_handlers)
    .add_for_types(**social_handlers)
    .add_for_types(**interaction_handlers)
    .apply
)
"""Represents the default process undertaken by an inbox item"""
