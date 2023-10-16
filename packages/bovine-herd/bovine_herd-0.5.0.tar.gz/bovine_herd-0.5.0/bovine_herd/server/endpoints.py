import logging

import bovine
from bovine.jsonld import with_bovine_context
from bovine.types import Visibility
from bovine_process.types import ProcessingItem
from bovine_store.types import EndpointType
from quart import Blueprint, current_app, g, make_response, redirect, request

from .objects.collection import collection_response
from .utils import path_from_request


logger = logging.getLogger(__name__)


async def proxy_url_response(actor):
    url = (await request.form)["id"]
    try:
        if url.startswith("acct:"):
            url, _ = await bovine.clients.lookup_uri_with_webfinger(actor.session, url)
        elif not url.startswith("http") and "@" in url:
            url = await bovine.clients.lookup_account_with_webfinger(actor.session, url)

        result = await actor.retrieve(url, include=["object", "actor", "attributedTo"])
        if result:
            return with_bovine_context(result), 200
        return {"status": "not found"}, 404
    except Exception as e:
        logger.error("Something went wrong during proxy url")
        logger.exception(e)
        return {"status": "something went wrong"}, 400


async def handle_event_source(endpoint_path, actor):
    if endpoint_path != actor["endpoints"]["eventSource"]:
        return {"status": "unauthorized"}, 401

    logger.info("Opening event source for %s", actor["name"])

    if "bovine_pub_sub" not in current_app.config:
        return {"status": "not implemented"}, 501

    pubsub = current_app.config["bovine_pub_sub"]

    response = await make_response(
        pubsub.event_stream(endpoint_path),
        {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked",
        },
    )
    response.timeout = None

    # last_event_id = request.headers.get("last-event-id")
    # if last_event_id:
    #     current_app.add_background_task(
    #         enqueue_missing_events, queue, last_event_id, actor["name"]
    #     )
    return response


def build_endpoints_blueprint(
    handle_outbox_item, start_background_task_inbox, start_background_task_outbox
):
    endpoints = Blueprint("endpoint", __name__)

    @endpoints.get("/<identifier>")
    async def endpoints_get(identifier):
        endpoint_path = path_from_request(request)
        object_store = current_app.config["bovine_store"]

        endpoint_type, actor = await object_store.resolve_endpoint_no_cache(
            endpoint_path
        )

        if endpoint_type is None:
            return (
                {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "Object",
                    "id": endpoint_path,
                    "name": "Ceci n'est pas un object",
                },
                404,
                {"content-type": "application/activity+json"},
            )

        if endpoint_type == EndpointType.ACTOR:
            logger.info("Getting %s for %s", endpoint_path, g.retriever)

            if endpoint_path == g.retriever:
                return (
                    actor.actor_object.build(visibility=Visibility.OWNER),
                    200,
                    {"content-type": "application/activity+json"},
                )

            if g.retriever is None or g.retriever == "NONE":
                if "text" in request.headers.get("accept", ""):
                    if actor.actor_object.url is not None:
                        return redirect(actor.actor_object.url)
                return {"status": "unauthorized"}, 401

            return (
                actor.actor_object.build(visibility=Visibility.PUBLIC),
                200,
                {"content-type": "application/activity+json"},
            )

        if endpoint_type == EndpointType.EVENT_SOURCE:
            actor = actor.actor_object.build(visibility=Visibility.OWNER)
            if g.retriever != actor["id"]:
                return {"status": "unauthorized"}, 401
            return await handle_event_source(endpoint_path, actor)

        return await collection_response(endpoint_path)

    @endpoints.post("/<identifier>")
    async def endpoints_post(identifier):
        if not g.retriever:
            return {"status": "unauthorized"}, 401

        endpoint_path = path_from_request(request)
        object_store = current_app.config["bovine_store"]

        endpoint_type, actor = await object_store.resolve_endpoint(endpoint_path)

        if endpoint_type not in [
            EndpointType.INBOX,
            EndpointType.OUTBOX,
            EndpointType.PROXY_URL,
        ]:
            return {"status": "method not allowed"}, 405

        if endpoint_type == EndpointType.INBOX:
            item = ProcessingItem(g.retriever, await request.get_json())
            await start_background_task_inbox(item, actor)

            return {"status": "processing"}, 202

        if g.retriever != actor.actor_object.id:
            return {"status": "unauthorized"}, 401

        if endpoint_type == EndpointType.OUTBOX:
            item = ProcessingItem(g.retriever, await request.get_json())
            item = await handle_outbox_item(item, actor)
            await start_background_task_outbox(item, actor)

            return (
                {"status": "created"},
                201,
                {"location": item.meta.get("object_location")},
            )

        if endpoint_type == EndpointType.PROXY_URL:
            return await proxy_url_response(actor)

    return endpoints
