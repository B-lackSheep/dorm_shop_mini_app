from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.mypy.util import serialize_type
from sqlalchemy.orm import selectinload
from unicodedata import category

from models import async_session, User, Product, Category, ProductVariant
from pydantic import BaseModel, ConfigDict
from typing import List



class CategorySchema(BaseModel):
    id: int
    category_name: str

    model_config = ConfigDict(from_attributes=True)


class ProductVariantSchema(BaseModel):
    id: int
    volume: str
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class ProductSchema(BaseModel):
    id: int
    product_name: str

    category: CategorySchema
    variants: List[ProductVariantSchema]

    model_config = ConfigDict(from_attributes=True)


async def get_product_info(product_id):
    async with async_session() as session:
        product = await session.scalar(
            select(Product)
            .where(Product.id == product_id)
            .options(
                selectinload(Product.variants),
                selectinload(Product.category)
            )
        )

        serialized_product = [
            ProductSchema.model_validate(product).model_dump()
        ]

        return serialized_product


async def add_product(admin_draft):
    async with async_session() as session:
        async with session.begin():
            category_name = admin_draft.get("category_name")
            category_stmt = select(Category).where(Category.category_name == category_name)
            category = await session.scalar(category_stmt)

            if not category:
                category = Category(category_name=category_name)
                session.add(category)
                await session.flush()

            product_name = admin_draft.get("product_name")
            product_stmt = select(Product).where(Product.product_name == product_name)
            product = await session.scalar(product_stmt)

            if not product:
                product = Product(product_name=product_name, category_id=category.id)
                session.add(product)
                await session.flush()

            variant = ProductVariant(
                product_id=product.id,
                volume=admin_draft.get("volume"),
                price=admin_draft.get("price"),
                quantity=admin_draft.get("quantity")
            )
            session.add(variant)

        await session.commit()

