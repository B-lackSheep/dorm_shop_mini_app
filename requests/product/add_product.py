from sqlalchemy import select
from models.db_models import Product, Category, ProductVariant


async def add_product(product_data, session):
    async with session.begin():
        category_name = product_data.get("category_name")
        category = await session.scalar(
            select(Category)
            .where(Category.category_name == category_name)
        )

        if not category:  # вроде и нужно, а вроде и перегруз
            category = Category(category_name=category_name)
            session.add(category)
            await session.flush()

        product_name = product_data.get("product_name")
        product = await session.scalar(
            select(Product)
            .where(Product.product_name == product_name)
        )

        if not product:
            product = Product(
                product_name=product_name,
                category_id=category.id
            )
            session.add(product)
            await session.flush()

        variant = ProductVariant(
            product_id=product.id,
            volume=product_data.get("volume"),
            price=product_data.get("price"),
            quantity=product_data.get("quantity")
        )
        session.add(variant)
    return {"status": "success", "message": "Product added"}
