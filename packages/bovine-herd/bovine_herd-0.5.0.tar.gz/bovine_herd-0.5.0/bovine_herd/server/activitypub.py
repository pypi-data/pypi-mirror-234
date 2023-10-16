import logging
from importlib.metadata import version as meta_version

import werkzeug
from .utils import path_from_request
from quart import Blueprint, current_app, request

activitypub = Blueprint("activitypub", __name__, url_prefix="/activitypub")
"""Provides the endpoints

- GET /<actor_name>
- GET /nodeinfo2_0

the second one returns a nodeinfo 2.0 response. The first
one returns a 404 not found except for bovine, when it returns
the application actor."""

logger = logging.getLogger(__name__)


@activitypub.get("/<account_name>")
async def userinfo(account_name: str) -> tuple[dict, int] | werkzeug.Response:
    if account_name != "bovine":
        return {"status": "not found"}, 404

    store = current_app.config["bovine_store"]
    path = path_from_request(request)
    actor = await store.application_actor_for_url(path)

    return (
        actor.actor_object,
        200,
        {"content-type": "application/activity+json"},
    )


@activitypub.get("/nodeinfo2_0")
async def nodeinfo() -> dict:
    user_count = 0

    if "bovine_store" in current_app.config:
        user_manager = current_app.config["bovine_store"]
        if user_manager:
            user_count = await user_manager.user_count()

    user_stat = {
        "total": user_count,
        "activeMonth": user_count,
        "activeHalfyear": user_count,
    }

    return {
        "metadata": {},
        "openRegistrations": False,
        "protocols": ["activitypub"],
        "services": {"inbound": [], "outbound": []},
        "software": {"name": "bovine", "version": meta_version("bovine_herd")},
        "usage": {"users": user_stat},
        "version": "2.0",
    }
