from pydantic import BaseModel
from typing import Optional

class FoodBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True
    category_id: int

class FoodCreate(FoodBase):
    pass

# What the API sends back to the user browsing the menu
class FoodOut(FoodBase):
    id: int

    class Config:
        from_attributes = True

class FoodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    category_id: Optional[int] = None

# Schema for Category
class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True