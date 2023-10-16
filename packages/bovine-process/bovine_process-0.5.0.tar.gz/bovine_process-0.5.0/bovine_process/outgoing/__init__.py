from bovine_process.utils.processor_list import ProcessorList
from bovine.jsonld import with_bovine_context

from .following import accept_follow, undo_follow
from .outgoing_delete import outgoing_delete
from .outgoing_update import outgoing_update
from .store_outgoing import add_outgoing_to_outbox, store_outgoing
from .update_id import update_id


async def sanitize(item, actor):
    item.data = with_bovine_context(item.data)
    return item


default_outbox_process = (
    ProcessorList()
    .add(sanitize)
    .add(update_id)
    .add(store_outgoing)
    .add(add_outgoing_to_outbox)
    .add_for_types(
        Update=outgoing_update,
        Delete=outgoing_delete,
    )
    .apply
)
"""Defines the synchrnous part of sending an outgoing object"""


default_async_outbox_process = (
    ProcessorList().add_for_types(Accept=accept_follow, Undo=undo_follow).apply
)
