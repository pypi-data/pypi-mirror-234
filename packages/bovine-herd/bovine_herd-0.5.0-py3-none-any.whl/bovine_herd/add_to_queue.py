import json
import logging

from bovine.types import ServerSentEvent, Visibility
from quart import current_app

from bovine_process.types import ProcessingItem

logger = logging.getLogger(__name__)


async def add_to_queue(item: ProcessingItem, *args) -> ProcessingItem | None:
    """If current.app.config["bovine_pub_sub"] is set, adds the item to
    a queue

    FIXME: Improve logic on how the queue is chosen
    FIXME: event-id logic"""
    if "bovine_pub_sub" not in current_app.config:
        return item

    actor = args[-1]

    pubsub = current_app.config["bovine_pub_sub"]

    data_s = json.dumps(item.data)
    event = ServerSentEvent(data=data_s, event="inbox")

    if "database_id" in item.meta:
        event.id = item.meta["database_id"]

    actor = actor.actor_object.build(visibility=Visibility.OWNER)
    event_source = actor["endpoints"]["eventSource"]

    await pubsub.send(event_source, event.encode())

    return item
