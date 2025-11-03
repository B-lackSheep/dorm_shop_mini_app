from config import app
from models.api_models import OrderItemRequest, OrderRequest, UserRequest
from models.db_models import async_session
from requests.order.add_order import add_order
from requests.user.find_user import find_user
from services.serialize_products import serialize_products


@app.get("/category/{category_id}/{tg_id}")
async def get_category(category_id):
    try:
        products = await serialize_products(category_id)

        if not products:
            return {"status": "error", "message": "Products in category not found"}

        return {"status": "success", "data": products}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/order/placed/{tg_id}")
async def order_placed(order_data: OrderRequest, order_components: OrderItemRequest,  user_data: UserRequest):
    async with async_session() as session:
        try:
            user = await find_user(user_data.tg_id, session)
            if not user:
                return {"status": "error", "message": "User not found"}

            result = await add_order(order_data, order_components, user_data, session)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}
