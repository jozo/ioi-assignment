from sqlalchemy import BigInteger, Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    currency = Column(String(10), nullable=False)
    date_ = Column(BigInteger, nullable=False)
    price = Column(Float, nullable=False)
