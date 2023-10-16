from urllib.parse import urlencode
from bovine.activitystreams import OrderedCollection, OrderedCollectionPage


async def ordered_collection_responder(url, count_coroutine, items_coroutine, **kwargs):
    if any(
        kwargs.get(name) is not None for name in ["first", "last", "min_id", "max_id"]
    ):
        return await ordered_collection_page(
            url,
            count_coroutine,
            items_coroutine,
            **kwargs,
        )

    count = await count_coroutine()

    builder = OrderedCollection(id=url, count=count)

    if count < 10:
        data = await items_coroutine()
        builder.items = data["items"]
    else:
        builder.first = f"{url}?first=1"
        builder.last = f"{url}?last=1"

    return builder.build(), 200, {"content-type": "application/activity+json"}


async def ordered_collection_page(url, count_coroutine, items_coroutine, **kwargs):
    data = await items_coroutine(**kwargs)
    builder = OrderedCollectionPage(
        id=url + "?" + urlencode(kwargs), items=data["items"], part_of=url
    )

    if "prev" in data:
        builder.prev = f"{url}?{data['prev']}"

    if "next" in data:
        builder.next = f"{url}?{data['next']}"

    return builder.build(), 200, {"content-type": "application/activity+json"}
