from unittest.mock import AsyncMock

import ccxt
from ward import raises, test

from api.exchange import ExchangeService


@test("Exchange can return BID price")
async def _():
    exchange_mock = AsyncMock()
    exchange_mock.fetch_ticker.return_value = {"bid": 4.2}
    service = ExchangeService(exchange_mock)

    assert await service.bid("IOI") == 4.2


@test("Exchange.bid() handles wrong currency")
async def _():
    exchange_mock = AsyncMock()
    exchange_mock.fetch_ticker.side_effect = ccxt.BadSymbol("Wrong currency")
    service = ExchangeService(exchange_mock)

    with raises(Exception) as ex:
        await service.bid("UNKNOWN")

    assert str(ex.raised) == "Exchange: Unsupported currency 'UNKNOWN'"
