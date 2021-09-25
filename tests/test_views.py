from unittest.mock import AsyncMock

from ward import test

from api import view


@test("API /price/currency - happy path")
async def _():
    exchange = AsyncMock()
    exchange.bid.return_value = 4.2
    d = {"exchange": exchange}
    request = AsyncMock()
    request.app.__getitem__.side_effect = d.__getitem__

    response = await view.price(request)

    assert response.status == 200
