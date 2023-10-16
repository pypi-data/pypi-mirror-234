from urllib.parse import urljoin, urlparse


def path_from_request(request) -> str:
    """Given a request (from quart) determines the url it is comming from.
    Main goal is to abstract away http vs https"""

    url = request.url
    if request.headers.get("X-Forwarded-Proto") == "https":
        url = url.replace("http://", "https://")

    return urljoin(url, urlparse(url).path)
