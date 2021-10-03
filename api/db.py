import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from api import settings
from api.models import Currency

log = logging.getLogger(__name__)


def get_session(db: AsyncEngine):
    return sessionmaker(db, expire_on_commit=False, class_=AsyncSession)


async def save_price(currency: str, bid: float, timestamp: int, db: AsyncEngine):
    try:
        async with get_session(db)() as session:
            session.add(Currency(currency=currency, price=bid, date_=timestamp))
            await session.commit()
    except SQLAlchemyError:
        log.exception("Can't save price to DB")


async def fetch_history(page: int, db: AsyncEngine):
    items = []
    async with get_session(db)() as session:
        stmt = (
            select(Currency)
            .order_by(Currency.id.desc())
            .slice(page * settings.PAGE_SIZE, (page + 1) * settings.PAGE_SIZE)
        )
        rows = await session.execute(stmt)
        for currency in rows.scalars().all():
            items.append(
                {
                    "currency": currency.currency,
                    "bid": currency.price,
                    "timestamp": currency.date_,
                }
            )
    return items
