from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.services.order_service import create_order

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])

# Schema for adding items
class CartItemAdd(BaseModel):
    food_id: int
    quantity: int = 1

@router.get("/")
def view_cart(request: Request):
    """View the current content of the session cart."""
    # This retrieves the cart from the session, or default returns to an empty dictionary
    cart = request.session.get("cart", {})
    return {"cart": cart}

@router.post("/add")
def add_to_cart(item: CartItemAdd, request: Request):
    cart = request.session.get("cart", {})

    # Session dictionary keys is saved always as string
    food_id_str = str(item.food_id)

    #If item is already in the cart, add (+) to the quantity. Otherwise set it
    if food_id_str in cart:
        cart[food_id_str] += item.quantity
    else:
        cart[food_id_str] = item.quantity

    # Save back to Session
    request.session["cart"] = cart
    return {"message": "Item added to cart", "cart": cart}

@router.delete("/remove/{food_id}")
def remove_from_cart(food_id: int, request: Request):
    """ To remove a specific item from the cart entirely."""
    cart = request.session.get("cart", {})
    food_id_str = str(food_id)

    if food_id_str in cart:
        del cart[food_id_str]
        request.session["cart"] = cart
        return {"message": "Item removed", "cart": cart}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found in cart"
    )

@router.post("/checkout")
def checkout(request: Request,  db: Session = Depends(get_db)):
    """"
      Convert the session cart into a real database order..
      Note: user_id is passed manually here for testing until i build JWT Login.
    """
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You must be logged in to checkout"
        )
    
    cart = request.session.get("cart", {})
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your cart is empty."
        )
    
    # This Format the session dict into the list format the order_service expects.
    # e.g.. {"1": 2, "4": 1} --> [{"food_id": 1, "quantity": 2}, {"food_id": 4, "quanity": 1}]
    formatted_items = [{"food_id": int(f_id), "quantity": int( qty)} for f_id, qty in cart.items()]

    new_order = create_order(db, user_id=user_id, cart_items=formatted_items)

    # If successful, empty the cart
    request.session.pop("cart", None)

    return {
        "message": "Order placed successfully!!",
        "order_id": new_order.id,
        "total_amount": new_order.total_amount
    }