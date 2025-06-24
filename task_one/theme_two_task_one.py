import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import String, Integer, ForeignKey, Float, CheckConstraint, Text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

load_dotenv()

DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

engine = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Genre(Base):
    __tablename__ = 'genres'

    genre_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_genre: Mapped[str] = mapped_column(String(255), nullable=False)

    books = relationship('Book', back_populates='genre')


class Author(Base):
    __tablename__ = 'authors'

    author_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_author: Mapped[str] = mapped_column(String(255), nullable=False)

    books = relationship('Book', back_populates='author')


class City(Base):
    __tablename__ = 'cities'

    city_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_city: Mapped[str] = mapped_column(String(255), nullable=False)
    days_delivery: Mapped[int] = mapped_column(Integer, nullable=False)

    clients = relationship('Client', back_populates='city')


class Book(Base):
    __tablename__ = 'books'

    book_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('authors.author_id'))
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey('genres.genre_id'))
    price: Mapped[float] = mapped_column(Float, CheckConstraint("price > 0"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, CheckConstraint("amount >= 0"), nullable=False)

    author = relationship('Author', back_populates='books')
    genre = relationship('Genre', back_populates='books')
    buy_books = relationship('BuyBook', back_populates='book')


class Client(Base):
    __tablename__ = 'clients'

    client_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_client: Mapped[str] = mapped_column(String(255), nullable=False)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.city_id'))
    email: Mapped[str] = mapped_column(String(255), nullable=False)

    city = relationship('City', back_populates='clients')
    buys = relationship('Buy', back_populates='client')


class Buy(Base):
    __tablename__ = 'buys'

    buy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    buy_description: Mapped[str] = mapped_column(Text, nullable=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('clients.client_id'))

    client = relationship('Client', back_populates='buys')
    buy_books = relationship('BuyBook', back_populates='buy')
    buy_steps = relationship('BuyStep', back_populates='buy')


class Step(Base):
    __tablename__ = 'steps'

    step_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_step: Mapped[str] = mapped_column(String(255), nullable=False)

    buy_steps = relationship('BuyStep', back_populates='step')


class BuyBook(Base):
    __tablename__ = 'buy_books'

    buy_book_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    buy_id: Mapped[int] = mapped_column(Integer, ForeignKey('buys.buy_id'))
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.book_id'))
    amount: Mapped[int] = mapped_column(Integer, CheckConstraint("amount > 0"), nullable=False)

    buy = relationship('Buy', back_populates='buy_books')
    book = relationship('Book', back_populates='buy_books')


class BuyStep(Base):
    __tablename__ = 'buy_steps'

    buy_step_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    buy_id: Mapped[int] = mapped_column(Integer, ForeignKey('buys.buy_id'))
    step_id: Mapped[int] = mapped_column(Integer, ForeignKey('steps.step_id'))
    date_step_beg: Mapped[datetime] = mapped_column(nullable=False)
    date_step_end: Mapped[datetime | None] = mapped_column(nullable=True)

    buy = relationship('Buy', back_populates='buy_steps')
    step = relationship('Step', back_populates='buy_steps')
