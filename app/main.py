from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.api import auth, foods, cart, orders
from app.database import SessionLocal, engine, Base
import os
from dotenv import load_dotenv
from app.config import settings

from app.services.food_service import create_category


load_dotenv()


# Create the database table on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chucks Kitchen API")
print("FastAPI app initialized")

app.include_router(auth.router)
app.include_router(foods.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        categories = ["Sides", "Main Dish", "Drinks", "Desserts"]
        for cat_name in categories:
            create_category(db, name=cat_name)
        print("✓ Essential categories seeded successfully.")
    finally:
        db.close()


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="chucks_cart_session",
    max_age=3600 # Session expires after 1 hour
)

@app.get("/")
def root():
    return {"message": "Welcome to Chucks Kitchen API"}