import logging

from aiohttp import web

from api import view
from api.exchange import exchange_context


def setup_app():
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    app.cleanup_ctx.append(exchange_context)
    app.router.add_get("/price/{currency}", view.price)
    return app


app = setup_app()


if __name__ == "__main__":
    web.run_app(app)
