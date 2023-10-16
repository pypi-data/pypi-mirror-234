from unittest.mock import AsyncMock, patch
from quart import g

from bovine_store.utils.test import store  # noqa F401
from bovine_herd.utils.test import test_app  # noqa F801

from bovine_store import BovineStore

from .authorize import add_authorization


async def test_add_authorization(test_app):  # noqa F401
    test_app.config["validate_http_signature"] = AsyncMock()

    async with test_app.test_request_context("/"):
        await add_authorization()

    test_app.config["validate_http_signature"].assert_awaited_once()


@patch("bovine.utils.date.check_max_offset_now")
async def test_add_authorization_moo_auth_1(mock, test_app):  # noqa F401
    test_app.config["validate_http_signature"] = AsyncMock()
    test_app.config["bovine_store"] = AsyncMock(BovineStore)
    test_app.config["bovine_store"].get_account_url_for_identity.return_value = (
        "acct:name",
        "mock",
    )

    headers = {
        "Date": "Wed, 15 Mar 2023 17:28:15 GMT",
        "Host": "myhost.tld",
        "Authorization": "Moo-Auth-1 did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5",  # noqa
        "X-Moo-Signature": "z5ahdHCbP9aJEsDtvG1MEZpxPzuvGKYcdXdKvMq5YL21Z2umxjs1SopCY2Ap8vZxVjTEf6dYbGuB7mtgcgUyNdBLe",  # noqa
    }
    async with test_app.test_request_context(
        "/path/to/resource", method="GET", headers=headers
    ):
        await add_authorization()

        assert g.retriever == "mock"

    test_app.config["validate_http_signature"].assert_not_awaited()


@patch("bovine.utils.date.check_max_offset_now")
async def test_add_authorization_moo_auth_1_post(mock, test_app):  # noqa F401
    test_app.config["validate_http_signature"] = AsyncMock()
    test_app.config["bovine_store"] = AsyncMock(BovineStore)
    test_app.config["bovine_store"].get_account_url_for_identity.return_value = (
        "name",
        "mock",
    )

    headers = {
        "Date": "Wed, 15 Mar 2023 17:28:15 GMT",
        "Host": "myhost.tld",
        "Digest": "sha-256=MILb5lUDD6Z0pDSxhgxj+hMBEw0uTzP3g2qUJGHMp9k=",
        "Authorization": "Moo-Auth-1 did:key:z6MkekwC6R9bj9ErToB7AiZJfyCSDhaZe1UxhDbCqJrhqpS5",  # noqa
        "X-Moo-Signature": "z4vPkJaoaSVQp5DrMb8EvCajJcerW36rsyWDELTWQ3cYmaonnGfb8WHiwH54BShidCcmpoyHjanVRYNrXXXka4jAn",  # noqa
    }
    async with test_app.test_request_context(
        "/path/to/resource", method="POST", headers=headers, json={"cows": "good"}
    ):
        await add_authorization()

        assert g.retriever == "mock"

    test_app.config["validate_http_signature"].assert_not_awaited()
