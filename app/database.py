from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the SQLite URL
# The 'check_same_thread' argument is specific to SQLite to allowFastAPIs

SQLALCHEMY_DATABASE_URL = "sqlite:///./chucks_kitchen.db"

# Initialize the Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session Maker
# Use to create a new session for every request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the Declerative Base
# Models (User, Food, Order) will inherit from this Base
Base = declarative_base()

# Dependency to get database seesion in API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()