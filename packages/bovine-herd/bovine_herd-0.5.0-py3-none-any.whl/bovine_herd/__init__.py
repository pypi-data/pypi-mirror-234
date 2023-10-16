from typing import Awaitable

import aiohttp
from quart import Quart
from tortoise.contrib.quart import register_tortoise

from bovine.crypto import build_validate_http_signature
from bovine_store import BovineStore
from bovine_store.config import tortoise_config
from bovine_process import handle_outbox_item, process_inbox_item, process_outbox_item
from bovine_process.utils.processor_list import ProcessorList

from .server import default_configuration
from .server.endpoints import build_endpoints_blueprint
from .server.objects import objects_blueprint


from .server.authorize import add_authorization
from .server.retrieve_public_key import retrieve_public_key

from .add_to_queue import add_to_queue


async def configure_bovine_store(app: Quart):
    if "session" not in app.config:
        app.config["session"] = aiohttp.ClientSession()

    app.config["bovine_store"] = BovineStore(
        session=app.config["session"],
    )

    app.config["validate_http_signature"] = build_validate_http_signature(
        retrieve_public_key
    )


def build_default_background_task_inbox(app):
    async def start_background_task_inbox(item, actor):
        app.add_background_task(
            ProcessorList().add(process_inbox_item).add(add_to_queue).apply, item, actor
        )

    return start_background_task_inbox


def build_default_background_task_outbox(app):
    async def start_background_task_outbox(item, actor):
        app.add_background_task(
            ProcessorList().add(process_outbox_item).add(add_to_queue).apply,
            item,
            actor,
        )

    return start_background_task_outbox


def BovineHerd(
    app: Quart,
    start_background_task_inbox: Awaitable | None = None,
    start_background_task_outbox: Awaitable | None = None,
    handle_outbox_item: Awaitable = handle_outbox_item,
    db_url: str = "sqlite://bovine.sqlite3",
    retriever_blocker: Awaitable | None = None,
) -> Quart:
    """Configures the quart app to use bovine herd. Requires a bovine_store compatible
    store to be available at app.config["bovine_store"]. Configures the endpoints

    * /.well-known
    * /activitypub
    * /endpoints
    * /objects

    :param app: The quart app to add the endpoints to.
    :param process_inbox_item: awaitable that asynchronously handles Activities
        that arrived at an inbox endpoint
    :param handle_outbox_item: awaitable that synchronously handles Activities
        that arrived at an outbox endpoint. This function should add the new id
        of the Activity to the ProcessingItem, so it can be returened in the
        location header.
    :param process_outbox_item: awaitable that asynchronously handles Activities
        that arrived at an outbox endpoint
    :param db_url: The database connection
    :param retriever_blocker: a coroutine that can use g.retriever or other parts of
        a request to stop it from being processed
    """

    register_tortoise(
        app,
        config=tortoise_config(db_url),
        generate_schemas=True,
    )

    if not start_background_task_inbox:
        start_background_task_inbox = build_default_background_task_inbox(app)
    if not start_background_task_outbox:
        start_background_task_outbox = build_default_background_task_outbox(app)

    @app.before_serving
    async def startup():
        if "session" not in app.config:
            session = aiohttp.ClientSession()
            app.config["session"] = session
        await configure_bovine_store(app)

    @app.after_serving
    async def shutdown():
        await app.config["session"].close()

    app.register_blueprint(default_configuration)
    endpoints = build_endpoints_blueprint(
        handle_outbox_item,
        start_background_task_inbox,
        start_background_task_outbox,
    )
    app.register_blueprint(endpoints, url_prefix="/endpoints")
    app.register_blueprint(objects_blueprint, url_prefix="/objects")

    if retriever_blocker:

        async def authorize():
            result = await add_authorization()
            if result:
                return result
            return await retriever_blocker()

        app.before_request(authorize)
    else:
        app.before_request(add_authorization)

    return app
