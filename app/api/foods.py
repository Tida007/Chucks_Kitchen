from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.services import food_service
from app.schemas.food import CategoryOut, FoodCreate, FoodUpdate, FoodOut

router = APIRouter(prefix="/foods", tags=["Menu & Foods"])

@router.get("/", response_model=List[FoodOut])
def get_menu(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Fetch the available menu items with optional category filtering.
    """
    return food_service.list_foods(db, category_id=category_id, is_available=True)


@router.get("/categories", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    """"List all food categories ("Sides", "Main Dish", "Drinks", "Desserts")."""
    from app.models.food import Category
    return db.query(Category).all()


@router.get("/{food_id}", response_model=FoodOut)
def get_food(food_id: int, db: Session = Depends(get_db)):
    """"Fetch details of a specific food item by its ID."""
    return food_service.get_food_by_id(db, food_id)


# Admin endpoints (for managing menu items) - these will be protected with authentication in a real app
@router.post("/", response_model=FoodOut, status_code=status.HTTP_201_CREATED)
def add_food(food_data: FoodCreate, db: Session = Depends(get_db)):
    """Add a new food item to the menu."""
    return food_service.create_food(
        db,
        name=food_data.name,
        description=food_data.description,
        price=food_data.price,
        category_id=food_data.category_id,
    )

@router.patch("/{food_id}", response_model=FoodOut)
def update_food(food_id: int, food_data: FoodUpdate, db: Session = Depends(get_db)):
    update_dict = food_data.model_dump(exclude_unset=True)
    return food_service.update_food(db, food_id, **update_dict)