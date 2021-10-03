import logging.config

from aiohttp import web

from api import views
from api.context import db_context, exchange_context


def setup_app():
    setup_logging()
    application = web.Application()
    setup_context(application)
    setup_routes(application)
    return application


def setup_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {},
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {"ccxt": {"level": "WARNING"}},
            "root": {},
        }
    )


def setup_context(application: web.Application):
    application.cleanup_ctx.append(db_context)
    application.cleanup_ctx.append(exchange_context)


def setup_routes(application: web.Application):
    application.router.add_get("/price/history", views.history)
    application.router.add_get("/price/{currency}", views.price)


app = setup_app()

if __name__ == "__main__":
    web.run_app(app, port=8000)
