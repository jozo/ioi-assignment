import logging
from dataclasses import dataclass

import ccxt.async_support as ccxt

log = logging.getLogger(__name__)


class ExchangeError(Exception):
    pass


@dataclass
class Bid:
    value: float
    timestamp: int


class ExchangeService:
    def __init__(self, exchange):
        self.exchange: ccxt.Exchange = exchange

    async def close(self):
        await self.exchange.close()

    async def bid(self, currency: str) -> Bid:
        try:
            ticker = await self.exchange.fetch_ticker(f"{currency}/USDT")
            return Bid(ticker["bid"], ticker["timestamp"])
        except ccxt.BadSymbol as e:
            raise ExchangeError(f"Exchange: Unsupported currency '{currency}'") from e
        except ccxt.BaseError as e:
            raise ExchangeError(f"Exchange: Problem with communication") from e
        except Exception as e:
            raise ExchangeError(f"Exchange: Unknown error") from e
