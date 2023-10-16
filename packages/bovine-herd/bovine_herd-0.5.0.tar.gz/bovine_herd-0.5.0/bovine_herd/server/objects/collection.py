import logging

from quart import request, g

from .ordered_collection import ordered_collection_responder
from bovine_store.store.collection import collection_count, collection_items

logger = logging.getLogger(__name__)


async def collection_response(endpoint_path: str):
    """Returns the response for a GET request to the endpoint path.

    The endpoint_path is assumed to represent an ordered collection.
    The GET request can have the query parameters `first`, `last`,
    `mind_id`, `max_id` that are treated according to FIXME."""
    arguments = {
        name: request.args.get(name)
        for name in ["first", "last", "min_id", "max_id"]
        if request.args.get(name) is not None
    }

    logger.info("Retrieving %s for %s", endpoint_path, g.retriever)

    async def ccount():
        return await collection_count(g.retriever, endpoint_path)

    async def citems(**kwargs):
        return await collection_items(g.retriever, endpoint_path, **kwargs)

    return await ordered_collection_responder(
        endpoint_path,
        ccount,
        citems,
        **arguments,
    )
