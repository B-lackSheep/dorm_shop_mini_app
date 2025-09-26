import os
from dotenv import load_dotenv
from sqlalchemy import String, Text, BigInteger, ForeignKey, Integer, Numeric, DateTime
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime
import pytz
from typing import Optional


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


DEFAULT_VALUES = {
    "username": "Не установлен username",
    "first_name": "Нет данных об имени",
    "room": "Нет данных о комнате",
    "total_cost": 0.0,
    "order_components": "Нет товаров",
    "product_name": "Имя товара не задано",
    "quantity": 0,
    "volume": "Нет данных о массе/объеме",
    "product_price": 0.0
}


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(32), nullable=False, default=DEFAULT_VALUES["username"])
    first_name: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES["first_name"])
    room: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES["room"])

    orders: Mapped[list["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sales: Mapped[list["Sale"]] = relationship(back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    total_cost: Mapped[float] = mapped_column(Numeric(10, 2), default=DEFAULT_VALUES["total_cost"])
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.timezone('Europe/Minsk'))
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped[User] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_name: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES['product_name'])
    volume: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES['volume'])
    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=DEFAULT_VALUES['product_price']
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=DEFAULT_VALUES['quantity'])

    order: Mapped["Order"] = relationship(back_populates="items")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES["product_name"])

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    category: Mapped["Category"] = relationship(back_populates="products")
    variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    volume: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=DEFAULT_VALUES["quantity"])

    product: Mapped["Product"] = relationship(back_populates="variants")


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    total_cost: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=DEFAULT_VALUES['total_cost']
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.timezone('Europe/Minsk'))
    )
    user_room: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES['room'])
    user_name: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES['first_name'])

    user: Mapped[User] = relationship(back_populates="sales")
    items: Mapped[list["SaleItem"]] = relationship(back_populates="sale", cascade="all, delete-orphan")


class SaleItem(Base):
    __tablename__ = "sale_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id", ondelete="CASCADE"))
    product_name: Mapped[str] = mapped_column(Text, nullable=False)
    volume: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES['volume'])
    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=DEFAULT_VALUES['product_price']
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=DEFAULT_VALUES['quantity'])

    sale: Mapped["Sale"] = relationship("Sale", back_populates="items")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
