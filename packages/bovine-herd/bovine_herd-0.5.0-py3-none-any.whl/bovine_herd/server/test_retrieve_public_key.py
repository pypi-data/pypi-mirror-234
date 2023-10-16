from unittest.mock import AsyncMock

import json
import pytest
import uuid

from bovine_store.utils.test import store  # noqa F401
from bovine_herd.utils.test import test_app  # noqa F801
from .retrieve_public_key import retrieve_public_key


@pytest.mark.parametrize(
    "data", [{}, {"publicKey": {}}, {"publicKey": {"id": "public_key_url"}}]
)
async def test_retrieve_public_key_result_none(data, test_app):  # noqa F811
    data["id"] = "some_url"
    data["@context"] = [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1",
    ]

    async with test_app.test_request_context("/", method="GET"):
        response_mock = AsyncMock()
        test_app.config["session"].get.return_value = response_mock
        response_mock.status = 200
        response_mock.text.return_value = json.dumps(data)
        response_mock.raise_for_status = lambda: 1

        result = await retrieve_public_key(str(uuid.uuid4()))
        assert result == (None, None)

        test_app.config["session"].get.assert_awaited_once()


async def test_retrieve_public_key(test_app):  # noqa F811
    async with test_app.test_request_context("/", method="GET"):
        data = {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1",
            ],
            "id": "https://remote/item_1",
            "publicKey": {
                "id": "https://remote/item_1#public_key_url",
                "owner": "https://remote/item_1",
                "publicKeyPem": "public",
            },
        }
        response_mock = AsyncMock()
        test_app.config["session"].get.return_value = response_mock
        response_mock.status = 200
        response_mock.text.return_value = json.dumps(data)
        response_mock.raise_for_status = lambda: 1

        result = await retrieve_public_key("https://remote/item_1#public_key_url")
        assert result == ("public", "https://remote/item_1")

        test_app.config["session"].get.assert_awaited_once()

        result = await retrieve_public_key("https://remote/item_1#public_key_url")
        assert result == ("public", "https://remote/item_1")
        test_app.config["session"].get.assert_awaited_once()


async def test_retrieve_public_key_plemora(test_app):  # noqa F811
    async with test_app.test_request_context("/", method="GET"):
        data = {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://pleroma.1d4.us/schemas/litepub-0.1.jsonld",
                {"@language": "und"},
            ],
            "followers": "https://remote/internal/fetch/followers",
            "following": "https://remote/internal/fetch/following",
            "id": "https://remote/internal/fetch",
            "inbox": "https://remote/internal/fetch/inbox",
            "invisible": True,
            "manuallyApprovesFollowers": False,
            "name": "Pleroma",
            "preferredUsername": "internal.fetch",
            "publicKey": {
                "id": "https://remote/internal/fetch#main-key",
                "owner": "https://remote/internal/fetch",
                "publicKeyPem": "public",
            },
            "summary": "An internal service",
            "type": "Application",
            "url": "https://remote/internal/fetch",
        }
        response_mock = AsyncMock()
        test_app.config["session"].get.return_value = response_mock
        response_mock.status = 200
        response_mock.text.return_value = json.dumps(data)
        response_mock.raise_for_status = lambda: 1

        result = await retrieve_public_key("https://remote/internal/fetch#main-key")
        assert result == ("public", "https://remote/internal/fetch")

        test_app.config["session"].get.assert_awaited_once()

        result = await retrieve_public_key("https://remote/internal/fetch#main-key")
        assert result == ("public", "https://remote/internal/fetch")
        test_app.config["session"].get.assert_awaited_once()
