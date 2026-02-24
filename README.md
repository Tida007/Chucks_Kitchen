# Chucks Kitchen API

A modern, feature-rich REST API for a food ordering and delivery system built with **FastAPI** and **SQLAlchemy**. This project provides a complete backend solution for managing a restaurant's menu, user authentication, shopping cart, and order management.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Admin Features](#admin-features)
- [Development](#development)

## ✨ Features

### User Management & Authentication

- **User Registration & Email Verification**: New users can register with email and phone number
- **OTP-based Email Verification**: One-time password system for account verification
- **Secure Login**: Password authentication with bcrypt hashing
- **Session Management**: Session-based authentication with 1-hour expiration
- **Admin Promotion**: Script to elevate users to admin privileges

### Menu Management

- **Food Categories**: Pre-configured categories (Sides, Main Dish, Drinks, Desserts)
- **Menu Items**: Full CRUD operations for food items
- **Item Details**: Each food item includes name, description, and price
- **Category Filtering**: Browse menu items by category

### Shopping Cart

- **Add to Cart**: Store items in user session
- **Cart Management**: View, update, and remove items from cart
- **Session-based Storage**: Cart persists during user session (1 hour)

### Order Management

- **Order Creation**: Process orders from cart items
- **Order History**: Users can view their order history
- **Order Status**: Track order status and details
- **Admin Order Management**: Admin users can view and manage all orders

### Utilities

- **OTP Generation & Verification**: Secure one-time password handling
- **Referral System**: Support for referral tracking and rewards
- **Email Verification**: Automated OTP delivery for account verification

## 🛠 Tech Stack

| Component           | Technology    | Version       |
| ------------------- | ------------- | ------------- |
| **Framework**       | FastAPI       | 0.104.1       |
| **Server**          | Uvicorn       | 0.24.0        |
| **ORM**             | SQLAlchemy    | 2.0.46        |
| **Database**        | SQLite        | Built-in      |
| **Authentication**  | Bcrypt & JWT  | 5.0.0 & 3.5.0 |
| **Data Validation** | Pydantic      | 2.3.0         |

## 📁 Project Structure

```
Chucks_Kitchen/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app initialization & configuration
│   ├── config.py                 # Settings & environment configuration
│   ├── database.py               # Database engine & session setup
│   │
│   ├── api/                      # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication endpoints (register, login, verify)
│   │   ├── foods.py              # Menu & food endpoints
│   │   ├── cart.py               # Shopping cart endpoints
│   │   └── orders.py             # Order management endpoints
│   │
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py               # User model (email, phone, password, admin status)
│   │   ├── food.py               # Food & Category models
│   │   └── order.py              # Order model
│   │
│   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── user.py               # User schemas (UserCreate, UserLogin, UserOut)
│   │   ├── food.py               # Food schemas
│   │   └── order.py              # Order schemas
│   │
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py       # User registration, verification, login logic
│   │   ├── food_service.py       # Food CRUD operations
│   │   └── order_service.py      # Order processing logic
│   │
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── otp.py                # OTP generation & verification
│   │   └── referral.py           # Referral system utilities
│   │
│   └── __pycache__/              # Python cache (generated)
│
├── promote.py                    # Admin promotion script
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (create this)
├── chucks_kitchen.db             # SQLite database (generated on first run)
└── README.md                     # This file
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Create Environment Variables File

Create a `.env` file in the root directory:

```bash
# .env
SECRET_KEY=""
DATABASE_URL=sqlite:///./chucks_kitchen.db
```

## ▶️ Running the Application

### Start the Development Server

```bash
# Make sure your virtual environment is activated
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Automatic Data Seeding

On startup, the application automatically creates default categories:

- Sides
- Main Dish
- Drinks
- Desserts

## 📡 API Endpoints

### Authentication (`/auth`)

| Method | Endpoint           | Description           | Auth Required |
| ------ | ------------------ | --------------------- | ------------- |
| `POST` | `/auth/register`   | Register a new user   | ❌            |
| `POST` | `/auth/verify`     | Verify email with OTP | ❌            |
| `POST` | `/auth/login`      | User login            | ❌            |
| `POST` | `/auth/resend-otp` | Resend OTP code       | ❌            |

**Register Example:**

```json
POST /auth/register
{
  "email": "user@example.com",
  "phone": "+1234567890",
  "password": "securepassword123"
}
```

**Verify Example:**

```json
POST /auth/verify
{
  "email": "user@example.com",
  "otp_code": "123456"
}
```

**Login Example:**

```json
POST /auth/login
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Menu & Foods (`/foods`)

| Method   | Endpoint            | Description                                        | Auth Required |
| -------- | ------------------- | -------------------------------------------------- | ------------- |
| `GET`    | `/foods/`           | Get all menu items (with optional category filter) | ❌            |
| `GET`    | `/foods/categories` | Get all food categories                            | ❌            |
| `GET`    | `/foods/{food_id}`  | Get food item details                              | ❌            |
| `POST`   | `/foods/`           | Add new food item (Admin only)                     | ✅            |
| `PATCH`  | `/foods/{food_id}`  | Update food item (Admin only)                      | ✅            |
| `DELETE` | `/foods/{food_id}`  | Delete food item (Admin only)                      | ✅            |

**Get Menu Example:**

```
GET /foods/?category_id=1
```

### Shopping Cart (`/cart`)

| Method   | Endpoint          | Description               | Auth Required |
| -------- | ----------------- | ------------------------- | ------------- |
| `GET`    | `/cart/`          | View shopping cart        | ✅            |
| `POST`   | `/cart/`          | Add item to cart          | ✅            |
| `PATCH`  | `/cart/{item_id}` | Update cart item quantity | ✅            |
| `DELETE` | `/cart/{item_id}` | Remove item from cart     | ✅            |

### Orders (`/orders`)

| Method  | Endpoint             | Description                      | Auth Required |
| ------- | -------------------- | -------------------------------- | ------------- |
| `GET`   | `/orders/`           | Get user's order history         | ✅            |
| `GET`   | `/orders/{order_id}` | Get order details                | ✅            |
| `POST`  | `/orders/`           | Create new order from cart       | ✅            |
| `PATCH` | `/orders/{order_id}` | Update order status (Admin only) | ✅            |

### Root (`/`)

| Method | Endpoint | Description     |
| ------ | -------- | --------------- |
| `GET`  | `/`      | Welcome message |



## 🗄️ Database Schema

### Users Table

- `id` (Integer, Primary Key)
- `email` (String, Unique)
- `phone` (String)
- `password` (String, Hashed with bcrypt)
- `is_verified` (Boolean, Default: False)
- `is_admin` (Boolean, Default: False)
- `otp_code` (String, For email verification)
- `otp_expiry` (DateTime)
- `created_at` (DateTime)

### Food Table

- `id` (Integer, Primary Key)
- `name` (String)
- `description` (Text)
- `price` (Float)
- `category_id` (Integer, Foreign Key)
- `is_available` (Boolean, Default: True)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Category Table

- `id` (Integer, Primary Key)
- `name` (String, Unique)

### Order Table

- `id` (Integer, Primary Key)
- `user_id` (Integer, Foreign Key)
- `total_price` (Float)
- `status` (String, e.g., "pending", "processing", "completed")
- `created_at` (DateTime)
- `updated_at` (DateTime)


## 👨‍💼 Admin Features

### Promoting a User to Admin

Run the `promote.py` script to elevate a user to admin status:

```bash
python promote.py
```

Edit the `promote.py` file to change the target email address:

```python
admin = "your-admin-email@example.com"
```

### Admin Capabilities

Admin users can:

- ✅ Add new food items to the menu
- ✅ Update existing food items
- ✅ Delete food items
- ✅ View and manage all orders
- ✅ Update order statuses

## 💻 Development

### Code Structure Best Practices

This project follows a **layered architecture** pattern:

1. **API Layer** (`/api`) - HTTP request handlers and route definitions
2. **Services Layer** (`/services`) - Business logic and domain operations
3. **Models Layer** (`/models`) - Database ORM definitions
4. **Schemas Layer** (`/schemas`) - Request/response validation using Pydantic
5. **Utils Layer** (`/utils`) - Reusable utility functions (OTP, referrals)
6. **Database Layer** - SQLAlchemy configuration and session management

### Dependencies

All required packages are listed in `requirements.txt`. Key packages:

- **fastapi** - Web framework
- **sqlalchemy** - ORM
- **bcrypt** - Password hashing
- **pydantic** - Data validation
- **pytest** - Testing framework

## 📝 License

This project is built for Chucks Kitchen.

## 🆘 Support

For issues, questions, or feature requests, please:

1. Check existing documentation
2. Review system flow logic for flow diagram
3. Check the Swagger UI at `/docs` for interactive API documentation
4. Create an issue with detailed information

---