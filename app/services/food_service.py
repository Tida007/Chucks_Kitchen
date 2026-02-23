from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.food import Food, Category
from typing import List, Optional

# Fetch all food items with optional category filter
def list_foods(db: Session, category_id: Optional[int] = None, is_available: bool = True) :
    query = db.query(Food).filter(Food.is_available == is_available)

    if category_id:
        query = query.filter(Food.category_id == category_id)

    return query.all()

# Administrative Action
def create_category(db: Session, name: str):
    category = db.query(Category).filter(Category.name == name).first()
    if not category:
        category = Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category

def get_food_by_id(db: Session, food_id: int):
    """This fetches a specific food item or raises a 404 error."""
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item {food_id} not found"
        )
    return food

def create_food(db: Session, name: str, description: str, price: float, category_id: int):
    # Create a new menu item.
    new_food = Food(
        name=name,
        description=description,
        price=price,
        category_id=category_id,
        is_available=True,
    )
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food

def update_food_availability(db: Session, food_id: int, is_available: bool):
    food = get_food_by_id(db, food_id)
    food.is_available = is_available
    db.commit()
    db.refresh(food)
    return food

def update_food_details(db: Session, food_id: int, update_data: dict):
    food = get_food_by_id(db, food_id)

    # Loop through the dictionary and update onlythe fields provided
    for key, value in update_data.items():
        setattr(food, key, value)

        db.commit()
        db.refresh(food)
        return food
    
def validate_food_availability(db: Session, cart_items: List[dict]):
    # This checks if all items in the cart are available before checkout
    total_amount = 0.0
    validated_items = []

    for item in cart_items:
        food = db.query(Food).filter(Food.id == item["food_id"]).first()

        # check if it exists and is currently on the menu
        if not food or not food.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item {item.get('food_id')} is no longer available."
            )
        
        # Historical price tracking is handled in Order model
        item_total = food.price * item["quantity"]
        total_amount += item_total

        # food object for easier proccessing in the Order service
        validated_items.append({"food": food, "quantity": item["quantity"]})

    return total_amount, validated_items