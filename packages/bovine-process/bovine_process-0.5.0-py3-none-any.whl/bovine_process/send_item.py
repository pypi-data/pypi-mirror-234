import asyncio
import logging
import traceback

from bovine.activitystreams.utils import recipients_for_object, remove_public
from bovine.jsonld import with_external_context

logger = logging.getLogger(__name__)


async def get_inbox_for_recipient(actor, recipient):
    try:
        logger.info("Getting inbox for %s", recipient)
        remote = await actor.retrieve(recipient)
        return remote.get("inbox")
    except Exception as ex:
        logger.warning("Failed to fetch inbox for %s with %s", recipient, ex)
        return


async def send_to_inbox(actor, inbox, data):
    try:
        response = await actor.post(inbox, data)
        logger.info(await response.text())
    except Exception as ex:
        logger.warning("Sending to %s failed with %s", inbox, ex)
        for log_line in traceback.format_exc().splitlines():
            logger.warning(log_line)


async def determine_recipients(item, actor):
    recipients = recipients_for_object(item.data)
    recipients = remove_public(recipients)

    recipients = recipients | set(item.meta.get("additional_recipients", []))

    logger.debug("Recipients '%s'", "', '".join(recipients))

    endpoints = [x for x in recipients if x in actor.endpoints]

    if len(endpoints) > 0:
        recipients = {x for x in recipients if x not in endpoints}.union(
            await actor.resolve_endpoints(endpoints)
        )

    return {x for x in recipients if x != actor.actor_id}


async def send_outbox_item(item, actor):
    """Sends the item to all the specfied outboxes

    Collections are resolved if they are part of actor.endpoints and then
    resolved via actor.resolve_endpoints.

    inboxes from actors are fetched from the database or refetched
    """
    logger.info("Sending outbox item")

    recipients = await determine_recipients(item, actor)

    inboxes = [await get_inbox_for_recipient(actor, x) for x in recipients]
    inboxes = [x for x in inboxes if x]

    logger.info("Inboxes %s", " - ".join(inboxes))
    item.data = with_external_context(item.data)

    await asyncio.gather(*[send_to_inbox(actor, inbox, item.data) for inbox in inboxes])
