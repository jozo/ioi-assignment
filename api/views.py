import logging
from typing import Optional

from aiohttp import web
from sqlalchemy.exc import SQLAlchemyError
from yarl import URL

from api import db, settings
from api.exchange import ExchangeError

log = logging.getLogger(__name__)


async def price(request: web.Request) -> web.Response:
    """Returns bid price for the selected currency"""
    currency = request.match_info["currency"]
    try:
        exchange = request.app["exchange"]
        bid = await exchange.bid(currency)
    except ExchangeError as e:
        log.exception("Exchange error", extra={"currency": currency})
        return web.json_response({"error": str(e)}, status=400)

    response = web.json_response({"bid": bid.value, "timestamp": bid.timestamp})
    await response.prepare(request)
    await response.write_eof()
    await db.save_price(currency, bid.value, bid.timestamp, request.app["db_engine"])
    return response


async def history(request: web.Request) -> web.Response:
    """Returns list of saved bid prices"""
    page = int(request.query.getone("page", 0))

    try:
        items = await db.fetch_history(page, request.app["db_engine"])
    except SQLAlchemyError:
        log.exception("Can't fetch history of prices from DB")
        return web.json_response({"error": "Internal error"}, status=500)
    return web.json_response(
        {"items": items, "next": _next_page(request.rel_url, items, page)}
    )


def _next_page(url: URL, items: list, page: int) -> Optional[str]:
    if len(items) == settings.PAGE_SIZE:
        return str(url.with_query(page=page + 1))
    return None
