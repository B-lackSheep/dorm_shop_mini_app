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
