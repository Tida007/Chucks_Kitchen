from sqlalchemy.orm import Session
from fastapi import  HTTPException, status
from app.models.order import Order, OrderItem
from app.services.food_service import validate_food_availability

def create_order(db: Session, user_id: int, cart_items: list[dict]):
    """Transform the carts items into an order and save it to the database."""

    #Validate each item in the cart
    total_amount, validate_items = validate_food_availability(db, cart_items)

    if not validate_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your cart is empty or contains unavailable items."
        )
    
    # Create the order
    new_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending" # Default status  when order is first placed
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Create order items
    for item in validate_items:
        food = item["food"]
        order_item = OrderItem(
            order_id=new_order.id,
            food_id=food.id,
            quantity=item["quantity"],
            unit_price=food.price # Capture the price at the time of order
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)

    return new_order

def get_user_orders(db: Session, user_id: int):
    """Fetches all orders placed by a specific user."""
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()

# Order status transition
ORDER_TRANSITIONS = {
    "pending": ["confirmed", "cancelled"],
    "confirmed": ["preparing", "cancelled"],
    "preparing": ["out_for_delivery"],
    "out_for_delivery": ["completed"],
    "completed": [],
    "cancelled": []
}

def can_cancel_order(order_status: str) -> bool:
    """Check if order can be cancelled based on status"""
    cancellable_statuses = ["pending", "confirmed"]
    return order_status in cancellable_statuses


# Update Order
def update_order_status(db: Session, order_id: int, new_status: str):
    """Updates the status of an existing order. (e.g., pending, preparing, delivered)"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found."
        )
    
    # Validate status
    current_status = order.status

    if new_status not in ORDER_TRANSITIONS.get(current_status, []):
        order_transitions = ORDER_TRANSITIONS.get(current_status, [])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update order status from '{current_status}' to '{new_status}'. Valid transitions are: {order_transitions}"
        )
    
    # Update status
    order.status = new_status

    db.commit()
    db.refresh(order)

    return order

# Cancel Order completelly
def cancel_order(db: Session, order_id: int, user_id: int):
    """Cancel an order - user only can cancel own order"""

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # verify order belongs to current user
    if order.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your order"
        )
    
    # Check if order can be cancelled
    if not can_cancel_order(order.status):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel order with status '{order.status}.' Only 'pending' or 'confirmed' order can be cancelled"
        )
    
    # Mark order as cancelled
    order.status = "cancelled"

    db.commit()
    db.refresh(order)

    return order