from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models.user import User
from app.services import order_service
from app.services.auth_service import get_current_user
from app.schemas.order import OrderOut
from typing import List

router = APIRouter(prefix="/orders", tags=["Order"])

@router.get("/my-orders", response_model=List[OrderOut])
def list_my_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch all orders placed by the currently authenticated user."""
    return order_service.get_user_orders(db, user_id=current_user.id)