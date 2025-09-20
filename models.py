import os
from dotenv import load_dotenv
from sqlalchemy import String, Text, Float, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


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
    "total_order_cost": 0.0,
    "order_components": "Нет товаров",
    "product_name": "Имя товара не задано",
    "quantity": 0
}


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    username: Mapped[str] = mapped_column(String(32), nullable=False, default=DEFAULT_VALUES["username"])
    first_name: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES["first_name"])
    room: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES["room"])
    total_cost: Mapped[float] = mapped_column(Float, nullable=False, default=DEFAULT_VALUES["total_cost"])

    orders: Mapped[list["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"), nullable=False)

    total_order_cost: Mapped[float] = mapped_column(Float, default=DEFAULT_VALUES["total_order_cost"])
    order_components: Mapped[str] = mapped_column(Text, nullable=False, default=DEFAULT_VALUES["order_components"])

    user: Mapped[User] = relationship(back_populates="orders")


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
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=DEFAULT_VALUES["quantity"])

    product: Mapped["Product"] = relationship(back_populates="variants")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
