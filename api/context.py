import logging

from aiohttp import web
from ccxt import async_support as ccxt
from sqlalchemy.ext.asyncio import create_async_engine

from api import settings
from api.exchange import ExchangeService

log = logging.getLogger(__name__)


async def db_context(application: web.Application):
    log.debug("Creating DB engine")
    engine = create_async_engine(settings.API_DB_URL)
    application["db_engine"] = engine
    yield
    await application["db_engine"].dispose()
    log.debug("DB engine disposed")


async def exchange_context(application: web.Application):
    log.debug("Connecting to exchange")
    config = {"timeout": settings.EXCHANGE_TIMEOUT}
    exchange = getattr(ccxt, settings.EXCHANGE)(config)
    application["exchange"] = ExchangeService(exchange)
    yield
    await application["exchange"].close()
    log.debug("Closed connection to exchange")
