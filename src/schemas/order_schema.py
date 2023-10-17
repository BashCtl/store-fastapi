from pydantic import BaseModel
from typing import List
from src.schemas.pet_schema import PetRes

class OrderItem(BaseModel):
    pet_id: int


class OrderIn(BaseModel):
    user_id: int
    status: str
    complete: bool
    items: List[OrderItem]


class OrderItemOut(BaseModel):
    id: int
    order_id: int
    pet: PetRes


class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    complete: bool
    items: List[OrderItemOut]
