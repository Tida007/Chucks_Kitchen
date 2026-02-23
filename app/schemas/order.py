from pydantic import BaseModel
from typing import List
from datetime import datetime

# Schema for an individual item inside an order
class OrderItemOut(BaseModel):
    id: int
    food_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemOut] #This nest the items inside the order response

    class Config:
        from_attributes = True