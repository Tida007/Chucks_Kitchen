from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, delete
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Order(Base):
    __tablename__ ="orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)

    # Status of the order (e.g., pending, completed, cancelled)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    # Link back to the user who placed the order
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    # Save price here so historic(past) orders don't change
    # If Admin updates food prices later
    unit_price = Column(Float, nullable=False)

    # Relationship
    order = relationship("Order", back_populates="items")
    food = relationship("Food")