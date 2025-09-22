from sqlalchemy import select
from models import async_session, Product, Category, ProductVariant


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
        return {"status": "success", "message": "Product added"}
