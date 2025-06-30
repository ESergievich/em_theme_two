from datetime import datetime

from sqlalchemy import Integer, String, Float, Date, CheckConstraint, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

engine = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exchange_product_id: Mapped[str] = mapped_column(String)
    exchange_product_name: Mapped[str] = mapped_column(String)
    delivery_basis_name: Mapped[str] = mapped_column(String)
    volume: Mapped[float] = mapped_column(Float)
    total: Mapped[float] = mapped_column(Float)
    count: Mapped[int] = mapped_column(Integer)
    oil_id: Mapped[str] = mapped_column(String)
    delivery_basis_id: Mapped[str] = mapped_column(String)
    delivery_type_id: Mapped[str] = mapped_column(String)
    date: Mapped[Date] = mapped_column(String, CheckConstraint("date >= '2023-01-01'"))
    created_on: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    updated_on: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
