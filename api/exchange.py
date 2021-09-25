import logging

import ccxt.async_support as ccxt
from aiohttp import web

log = logging.getLogger(__name__)


class ExchangeError(Exception):
    pass


class ExchangeService:
    def __init__(self, exchange):
        self.exchange: ccxt.Exchange = exchange

    async def close(self):
        await self.exchange.close()

    async def bid(self, currency: str) -> float:
        try:
            ticker = await self.exchange.fetch_ticker(f"{currency}/USDT")
            return ticker["bid"]
        except ccxt.BadSymbol as e:
            raise ExchangeError(f"Exchange: Unsupported currency '{currency}'") from e
        except ccxt.BaseError as e:
            raise ExchangeError(f"Exchange: Problem with communication") from e
        except Exception as e:
            raise ExchangeError(f"Exchange: Unknown error") from e


async def exchange_context(app: web.Application):
    log.info("Connecting to exchange")
    app["exchange"] = ExchangeService(ccxt.kucoin())
    yield
    await app["exchange"].close()
    log.info("Closed connection to exchange")
