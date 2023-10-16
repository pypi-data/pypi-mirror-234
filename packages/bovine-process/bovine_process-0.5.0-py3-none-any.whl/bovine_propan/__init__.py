import os
import json
import aiohttp
import logging

from faststream import FastStream, Context
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue, ExchangeType
from faststream.annotations import Logger, ContextRepo


from bovine_process.types import ProcessingItem
from bovine_process import process_inbox_item
from bovine_process.outgoing import default_async_outbox_process
from bovine_process.send_item import (
    determine_recipients,
    send_to_inbox,
    get_inbox_for_recipient,
)
from bovine.types import ServerSentEvent, Visibility
from bovine.jsonld import with_external_context

from bovine_store.config import tortoise_config
from tortoise import Tortoise

from bovine_propan.actor import bovine_actor

logging.basicConfig(level=logging.INFO)

broker = RabbitBroker(os.environ.get("BOVINE_AMQP", "amqp://localhost"))
app = FastStream(broker)
"""faststream app can be run using 

.. code-block:: bash

    faststream run bovine_propan/__init__:app"""

exch = RabbitExchange("processing", auto_delete=False, type=ExchangeType.TOPIC)
processed = RabbitExchange("processed", auto_delete=False, type=ExchangeType.TOPIC)

inbox_queue = RabbitQueue("inbox", auto_delete=False, routing_key="inbox")
outbox_queue = RabbitQueue("outbox", auto_delete=False, routing_key="outbox")
to_send_queue = RabbitQueue("to_send", auto_delete=False, routing_key="to_send")


@app.on_startup
async def startup(context: ContextRepo):
    db_url = os.environ.get("BOVINE_DB_URL", "sqlite://bovine.sqlite3")
    await Tortoise.init(config=tortoise_config(db_url))
    await Tortoise.generate_schemas()

    session = aiohttp.ClientSession()
    context.set_global("session", session)


@app.on_shutdown
async def shutdown(session: aiohttp.ClientSession = Context()):
    await Tortoise.close_connections()
    session.close()


@broker.subscriber(inbox_queue, exch)
async def inbox_handler(
    body: dict, logger: Logger, session: aiohttp.ClientSession = Context()
):
    async with bovine_actor(body, session) as actor:
        item = ProcessingItem(body["submitter"], body["data"])
        await process_inbox_item(item, actor)

        data_s = json.dumps(item.data)
        event = ServerSentEvent(data=data_s, event="inbox")

        if "database_id" in item.meta:
            event.id = item.meta["database_id"]

        actor_info = actor.actor_object.build(visibility=Visibility.OWNER)
        event_source = actor_info["endpoints"]["eventSource"]

        await broker.publish(
            event.encode(), routing_key=event_source, exchange=processed
        )


@broker.subscriber(outbox_queue, exch)
async def outbox_handler(
    body: dict, logger: Logger, session: aiohttp.ClientSession = Context()
):
    async with bovine_actor(body, session) as actor:
        item = ProcessingItem(body["submitter"], body["data"])
        await default_async_outbox_process(item, actor)

        recipients = await determine_recipients(item, actor)
        to_send = with_external_context(item.data)

        for recipient in recipients:
            await broker.publish(
                {
                    "recipient": recipient,
                    "data": to_send,
                    "bovine_name": body["bovine_name"],
                },
                routing_key="to_send",
                exchange=exch,
            )

        data_s = json.dumps(item.data)
        event = ServerSentEvent(data=data_s, event="inbox")

        if "database_id" in item.meta:
            event.id = item.meta["database_id"]

        actor_info = actor.actor_object.build(visibility=Visibility.OWNER)
        event_source = actor_info["endpoints"]["eventSource"]

        await broker.publish(
            event.encode(), routing_key=event_source, exchange=processed
        )


@broker.subscriber(to_send_queue, exch)
async def to_send_handler(
    body: dict, logger: Logger, session: aiohttp.ClientSession = Context()
):
    async with bovine_actor(body, session) as actor:
        inbox = await get_inbox_for_recipient(actor, body["recipient"])
        if inbox:
            await send_to_inbox(actor, inbox, body["data"])
