from fastapi import APIRouter
from services.serialize_products import serialize_products


router = APIRouter(
    prefix="/category",
    tags=["Category"]
)


@router.get("/{category_id}")
async def get_category(category_id: int):
    try:
        products = await serialize_products(category_id)
        if not products:
            return {"status": "error", "message": "Products in category not found"}
        return {"status": "success", "data": products}
    except Exception as e:
        return {"status": "error", "message": str(e)}
