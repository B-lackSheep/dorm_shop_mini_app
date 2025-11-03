from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.api_models import ProductResponse, CategoryResponse, ProductVariantResponse
from models.db_models import async_session, Product, Category


async def get_products_by_category(category_id):
    async with async_session() as session:
        category_result = await session.execute(
            select(Category).where(Category.id == category_id)
        )
        category = category_result.scalar_one_or_none()

        if not category:
            return None

        products_result = await session.execute(
            select(Product)
            .options(
                selectinload(Product.variants),
                selectinload(Product.category)
            )
            .where(Product.category_id == category_id)
        )
        products = products_result.scalars().all()

        if not products:
            return None

        available_products = []
        for product in products:
            available_variants = [
                variant for variant in product.variants
                if variant.quantity > 0
            ]

            if available_variants:
                product_response = ProductResponse(
                    id=product.id,
                    product_name=product.product_name,
                    category=CategoryResponse.model_validate(product.category),
                    variants=[
                        ProductVariantResponse.model_validate(variant)
                        for variant in available_variants
                    ]
                )
                available_products.append(product_response)

        return available_products
