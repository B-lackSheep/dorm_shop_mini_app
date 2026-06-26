from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class OrderItemRequest(BaseModel):
    id: int
    order_id: int
    category_name: str
    product_name: str
    volume: str
    price: float
    quantity: int


class OrderRequest(BaseModel):
    id: int
    total_cost: float
    notes: Optional[str] = None


class UserRequest(BaseModel):
    id: int
    tg_id: int
    username: str
    first_name: str
    room: str


class PlaceOrderRequest(OrderRequest):
    items: list[OrderItemRequest]
    user: UserRequest


class CategoryResponse(BaseModel):
    id: int
    category_name: str

    model_config = ConfigDict(from_attributes=True)


class ProductVariantResponse(BaseModel):
    id: int
    volume: str
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    id: int
    product_name: str
    category: CategoryResponse
    variants: List[ProductVariantResponse]

    model_config = ConfigDict(from_attributes=True)
