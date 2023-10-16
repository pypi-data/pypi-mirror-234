from unittest.mock import MagicMock

from .utils import path_from_request


def test_path_from_request():
    request = MagicMock(url="http://localhost/some/path", headers={})

    assert path_from_request(request) == "http://localhost/some/path"

    request = MagicMock(
        url="http://localhost/some/path", headers={"X-Forwarded-Proto": "https"}
    )

    assert path_from_request(request) == "https://localhost/some/path"


def test_path_from_request_no_query():
    request = MagicMock(url="http://localhost/some/path?nothere=1", headers={})

    assert path_from_request(request) == "http://localhost/some/path"
