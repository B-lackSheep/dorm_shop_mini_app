from fastapi import APIRouter, Body
from typing import Annotated
from models.db_models import async_session
from models.api_models import PlaceOrderRequest
from requests.order.add_order import add_order
from requests.user.find_user import find_user
from services.print_order import print_order
from config import bot


router = APIRouter(
    prefix="/order",
    tags=["Order"]
)


@router.post("/placed")
async def order_placed(payload: PlaceOrderRequest):
    async with async_session() as session:
        try:
            user = await find_user(payload.user.tg_id, session)
            if not user:
                return {"status": "error", "message": "User not found"}

            result = await add_order(payload, payload.items, payload.user, session)

            text = await print_order(payload, payload.items, payload.user)
            await bot.send_message(payload.user.tg_id, text)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}
