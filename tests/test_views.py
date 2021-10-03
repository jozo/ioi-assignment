from unittest.mock import AsyncMock, patch

from aiohttp.test_utils import _create_app_mock, make_mocked_request
from sqlalchemy.exc import DisconnectionError
from ward import test

from api import views
from api.exchange import Bid, ExchangeError


def mock_app():
    app = _create_app_mock()
    exchange = AsyncMock()
    exchange.bid.return_value = Bid(4.2, 123456)
    app["exchange"] = exchange
    app["db_engine"] = AsyncMock()
    return app


@test("API /price/{currency}")
async def _():
    req = make_mocked_request(
        "GET", "/price/", match_info={"currency": "IOI"}, app=mock_app()
    )

    with patch("api.views.db", new_callable=AsyncMock) as mock_db:
        response = await views.price(req)

    assert response.status == 200
    assert response.body == b'{"bid": 4.2, "timestamp": 123456}'
    assert mock_db.save_price.called


@test("API /price/{currency} - exchange error")
async def _():
    app = mock_app()
    app["exchange"].bid.side_effect = ExchangeError("something wrong")
    req = make_mocked_request("GET", "/price/", match_info={"currency": "IOI"}, app=app)

    response = await views.price(req)

    assert response.status == 400
    assert response.body == b'{"error": "something wrong"}'


@test("API /price/history")
async def _():
    req = make_mocked_request("GET", "/price/history", app=mock_app())
    items = [
        {
            "currency": "IOI",
            "bid": 4.2,
            "timestamp": 123456,
        }
    ]
    with patch("api.views.db", new_callable=AsyncMock) as mock_db:
        mock_db.fetch_history.return_value = items
        response = await views.history(req)

    assert response.status == 200
    assert (
        response.body
        == b'{"items": [{"currency": "IOI", "bid": 4.2, "timestamp": 123456}], "next": null}'
    )
    assert mock_db.fetch_history.called


@test("API /price/history - db error")
async def _():
    req = make_mocked_request("GET", "/price/history", app=mock_app())
    with patch("api.views.db", new_callable=AsyncMock) as mock_db:
        mock_db.fetch_history.side_effect = DisconnectionError
        response = await views.history(req)

    assert response.status == 500
    assert response.body == b'{"error": "Internal error"}'
    assert mock_db.fetch_history.called
