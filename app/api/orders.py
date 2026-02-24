from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models.order import Order
from app.models.user import User
from app.services import order_service
from app.services.auth_service import get_admin_user, get_current_user
from app.schemas.order import OrderOut
from typing import List

router = APIRouter(prefix="/orders", tags=["Order"])

@router.get("/my-orders", response_model=List[OrderOut])
def list_my_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch all orders placed by the currently authenticated user."""
    return order_service.get_user_orders(db, user_id=current_user.id)

@router.get("/{order_id}", response_model=OrderOut)
def get_order_details(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    """Fetch Specific order by ID - user can only see their orders"""

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    return order

@router.patch("/{order_id}/status")
def update_order_status(order_id: int, new_status: str, admin_user: User = Depends(get_admin_user), db: Session = Depends(get_db)):

    """Update order status - ADMIN ONLY"""

    updated_order = order_service.update_order_status(db, order_id, new_status)

    return {
        "message": "Order status updated",
        "order_id": updated_order.id,
        "status": update_order_status
    }

@router.delete("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    """Cancel an order"""

    cancelled_order = order_service.cancel_order(
        db=db,
        order_id=order_id,
        user_id=current_user.id
    )

    return {
        "mesage": "Order cancelled sucessfully",
        "order_id": cancelled_order.id,
        "status": cancelled_order.status,
        "refund_amount": cancelled_order.total_amount
    }