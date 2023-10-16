import logging
from typing import Tuple
from quart import current_app, request
from asyncstdlib.functools import lru_cache

from bovine.jsonld import value_from_object
from .utils import path_from_request

logger = logging.getLogger(__name__)


async def refetch_public_key(app_actor, store, key_url: str) -> dict | None:
    data = await app_actor.get(key_url, fail_silently=True)
    if data is None:
        logger.info("Could not retrieve public key from %s", key_url)
        return None

    await app_actor.store_remote_actor(data)
    return data


@lru_cache
async def retrieve_public_key(key_url: str) -> Tuple[str | None, str | None]:
    store = current_app.config["bovine_store"]
    app_actor = await store.application_actor_for_url(path_from_request(request))

    try:
        data = await store.retrieve(app_actor.actor_id, key_url)
        if data is None or isinstance(data, str):
            data = await refetch_public_key(app_actor, store, key_url)
        if "publicKey" in data:
            data = data.get("publicKey", {})
    except Exception as e:
        logger.info(e)

        data = await refetch_public_key(app_actor, store, key_url)
        if data is None:
            return None, None

        if "publicKey" in data:
            data = data.get("publicKey", {})

    if data.get("id") != key_url:
        logger.warning(f"Public key id mismatches for {key_url} and {data.get('id')}")
        return None, None

    # FIXME: Is this necessary with a default context?

    publicKeyPem = value_from_object(data, "publicKeyPem")
    owner = value_from_object(data, "owner")

    return publicKeyPem, owner
