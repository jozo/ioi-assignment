import logging

from aiohttp import web

from api.exchange import ExchangeError

log = logging.getLogger(__name__)


async def price(request: web.Request) -> web.Response:
    currency = request.match_info["currency"]
    exchange = request.app["exchange"]

    try:
        bid = await exchange.bid(currency)
        return web.json_response({"bid": bid})
    except ExchangeError as e:
        log.exception("Exchange error", extra={"currency": currency})
        return web.json_response({"error": str(e)}, status=400)
