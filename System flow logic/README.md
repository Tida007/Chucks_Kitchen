## 🎯 Frontend-Backend Integration & Data Flow

This section illustrates how the frontend communicates with the backend for key user flows and screens. Use these diagrams as a reference for understanding data requirements and API interactions.

### Screen: User Registration & Email Verification

**Data Required for Frontend:**

- Email
- Phone Number
- Password
- OTP Code (for verification step)

**Frontend-to-Backend Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│ REGISTRATION SEQUENCE DIAGRAM                               │
└─────────────────────────────────────────────────────────────┘

Frontend                              Backend                 Database
   │                                    │                         │
   │─────────POST /auth/register───────>│                         │
   │  (email, phone, password)          │                         │
   │                                    ├──Check email exists──>│
   │                                    │<─────Query Response──┤
   │                                    │                         │
   │                                    ├──Hash password──┐        │
   │                                    │<─────Done───────┘        │
   │                                    │                         │
   │                                    ├──Generate OTP──┐         │
   │                                    │<──OTP(123456)──┘        │
   │                                    │                         │
   │                                    ├──Insert User──────────>│
   │                                    │<──Confirmed──────────┤
   │                                    │                         │
   │<─ 201 Created + User Object────────│                         │
   │  (Console: OTP Code: 123456)       │                         │
   │                                    │                         │
   │─────POST /auth/verify─────>        │                         │
   │ (email, otp_code)                  │                         │
   │                                    ├──Verify OTP──────────>│
   │                                    │<─Valid───────────────┤
   │                                    │                         │
   │                                    ├──Update is_verified──>│
   │                                    │<──Confirmed──────────┤
   │                                    │                         │
   │<─ 200 OK (Account Verified)────────│                         │
```

### Screen: Menu Display (Browse Foods)

**Data Required for Frontend:**

- Category ID (optional filter)

**Data Returned from Backend:**

```json
[
  {
    "id": 1,
    "name": "Fried Rice",
    "description": "Delicious fried rice with vegetables",
    "price": 1299,
    "category_id": 1,
    "category_name": "Main Dish",
    "is_available": true
  },
  ...
]
```

**Frontend-to-Backend Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│ MENU DISPLAY SYSTEM LOGIC                                   │
└─────────────────────────────────────────────────────────────┘

START
   │
   ├─> User Loads Menu Screen
   │
   ├─> Frontend sends: GET /foods/
   │   (optional: ?category_id=1)
   │
   └─> Backend Processing:
       │
       ├─> Check category filter exists
       │
       ├─> Query Database:
       │   SELECT * FROM foods
       │   WHERE is_available = true
       │   AND (category_id = ? OR category_id IS NULL)
       │
       ├─> Join with categories to get names
       │
       └─> Return List[FoodOut] with:
           - id, name, description, price
           - category_id, category_name
           - is_available status
   │
   ├─> Frontend receives response (200 OK)
   │
   ├─> Render Food Grid/List on Screen
   │
   └─> END
```

### Screen: Shopping Cart Management

**Data Required for Frontend (per request):**

- Food ID (to add)
- Quantity (to update)
- Cart Item ID (to remove)

**Cart State Data Structure:**

```json
{
  "user_id": 123,
  "items": [
    {
      "id": 1,
      "food_id": 5,
      "food_name": "Burger",
      "price": 6.99,
      "quantity": 2,
      "subtotal": 13.98
    }
  ],
  "total_items": 1,
  "total_price": 13.98
}
```

**Cart Operations Sequence:**

```
┌─────────────────────────────────────────────────────────────┐
│ SHOPPING CART USER FLOW                                     │
└─────────────────────────────────────────────────────────────┘

User Action             Frontend              Backend           Session
                          │                     │                 │
VIEW CART                 │                     │                 │
   │                      │                     │                 │
   └─────────────────────>│                     │                 │
                          ├──GET /cart/────────>│                 │
                          │                     ├─Query Cart──────>│
                          │                     │<──Cart Data──────┤
                          │<──200 + Cart Data───│                 │
                          │                     │                 │
                          └─ Display Cart Items                  │
                                                                 │
ADD TO CART                                                      │
   │                                                             │
   │ (selects Food: Burger, qty: 2)                             │
   │                                                             │
   └─────────────────────>│                                      │
                          ├──POST /cart/───────>│                │
                          │ {food_id: 5, qty: 2}│                │
                          │                     ├─Check Food───>│
                          │                     │<─Valid◄────────┤
                          │                     │                │
                          │                     ├─Add to Session>│
                          │                     │<─Done◄─────────┤
                          │<──201 + Item Added──│                │
                          │                     │                │
                          └─ Update Cart Display                 │
                                                                 │
CHANGE QUANTITY                                                  │
   │                                                             │
   │ (updates Burger qty: 2 → 3)                                │
   │                                                             │
   └─────────────────────>│                                      │
                          ├──PATCH /cart/1────>│                 │
                          │ {quantity: 3}      │                │
                          │                     ├─Update Session>│
                          │                     │<─Done◄─────────┤
                          │<──200 + Updated Item                 │
                          │                     │                │
                          └─ Refresh Cart Display                │
                                                                 │
REMOVE FROM CART                                                 │
   │                                                             │
   │ (removes Burger)                                           │
   │                                                             │
   └─────────────────────>│                                      │
                          ├──DELETE /cart/1───>│                 │
                          │                     ├─Remove Session>│
                          │                     │<─Done◄─────────┤
                          │<──204 No Content───│                 │
                          │                     │                │
                          └─ Remove Item from Display            │
```

### Screen: Checkout & Order Creation

**Data Required for Frontend:**

- Cart contents (already in session)
- Delivery address (optional in this version)
- User confirmation

**Order Data Returned:**

```json
{
  "id": 456,
  "user_id": 123,
  "items": [
    {
      "food_id": 5,
      "food_name": "Burger",
      "quantity": 2,
      "price": 6.99,
      "subtotal": 13.98
    }
  ],
  "total_price": 13.98,
  "status": "pending",
  "created_at": "2026-02-24T10:30:00"
}
```

**Order Creation Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│ CHECKOUT & ORDER PLACEMENT FLOWCHART                         │
└─────────────────────────────────────────────────────────────┘

START: User clicks "Place Order"
   │
   ├─ Is cart empty?
   │  ├─ YES → Show error "Cart is empty"
   │  │         Return to cart screen
   │  │
   │  └─ NO → Continue
   │
   ├─ Is user authenticated?
   │  ├─ NO → Redirect to login
   │  │       Return after login
   │  │
   │  └─ YES → Continue
   │
   ├─ Frontend sends: POST /orders/
   │  {cart_contents}
   │
   ├─ Backend Processing:
   │  │
   │  ├─ Verify all items still available
   │  │  ├─ Item not available?
   │  │  │  └─ Return error "Item no longer available"
   │  │  │
   │  │  └─ All items available → Continue
   │  │
   │  ├─ Calculate total price
   │  │
   │  ├─ Create order record in database
   │  │
   │  ├─ Store order details (items, prices, timestamp)
   │  │
   │  ├─ Clear shopping cart from session
   │  │
   │  └─ Return 201 + Order object
   │
   ├─ Frontend receives order confirmation
   │
   ├─ Show success screen with:
   │  - Order ID
   │  - Total price
   │  - Estimated delivery time
   │
   ├─ Clear local cart data
   │
   └─ END
```

### Screen: Login Screen

**Data Required for Frontend:**

- Email
- Password

**Response Data:**

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 123,
    "email": "user@example.com",
    "is_verified": true,
    "is_admin": false
  }
}
```

**Login Sequence Diagram:**

```
┌─────────────────────────────────────────────────────────────┐
│ LOGIN PROCESS                                               │
└─────────────────────────────────────────────────────────────┘

Frontend                         Backend                Database
   │                               │                        │
   │ User enters credentials       │                        │
   │                               │                        │
   ├──POST /auth/login────────────>│                        │
   │ {email, password}             │                        │
   │                               ├──Query user────────>│
   │                               │<──User record◄──────┤
   │                               │                        │
   │                               ├─Verify password       │
   │                               │ (bcrypt.compare)      │
   │                               │                        │
   │                Is password OK?                         │
   │                    │                                    │
   │                    ├─NO─────────>Return 400 error      │
   │                    │             "Invalid credentials" │
   │<─────────400 Unauthorized───────│                       │
   │                    │                                    │
   │                    └─YES────────>Create session         │
   │                                 │                        │
   │                                 ├─Set session cookie   │
   │                                 │                        │
   │<───────200 + User Info───────────│                      │
   │   (session_cookie)              │                      │
   │                                 │                       │
   ├─Store in browser storage        │                       │
   │                                 │                       │
   └─Redirect to home/dashboard      │                       │
```

### Screen: Admin - Manage Menu Items

**Data Required for Adding Food:**

```json
{
  "name": "Grilled Chicken",
  "description": "Tender grilled chicken breast",
  "price": 12.99,
  "category_id": 1
}
```

**Admin Operations Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│ ADMIN MENU MANAGEMENT                                       │
└─────────────────────────────────────────────────────────────┘

Admin User                Backend                  Database
    │                       │                          │
  ADD FOOD ITEM             │                          │
    │                       │                          │
    ├─POST /foods/─────────>│                          │
    │ {name, desc, price,   │                          │
    │  category_id}         ├─Verify admin user────>│
    │                       │<──is_admin=true◄──────┤
    │                       │                          │
    │                       ├─Validate data           │
    │                       │ (name, price > 0)       │
    │                       │                          │
    │                       ├─Insert into database──>│
    │                       │<──New food record◄─────┤
    │                       │                          │
    │<──201 + Food Object───│                          │
    │                       │                          │
  EDIT FOOD ITEM            │                          │
    │                       │                          │
    ├─PATCH /foods/5───────>│                          │
    │ {price: 13.99}        ├─Verify ownership        │
    │                       │ (is_admin)              │
    │                       │                          │
    │                       ├─Update database────────>│
    │                       │<──Success◄──────────────┤
    │                       │                          │
    │<──200 + Updated Item──│                          │
    │                       │                          │
  DELETE FOOD ITEM          │                          │
    │                       │                          │
    ├─DELETE /foods/5──────>│                          │
    │                       ├─Verify admin user       │
    │                       │                          │
    │                       ├─Remove from database───>│
    │                       │<──Success◄──────────────┤
    │                       │                          │
    │<──204 No Content──────│                          │
```

### Data Flow Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ COMPLETE SYSTEM ARCHITECTURE                                │
└─────────────────────────────────────────────────────────────┘

                         ┌──────────────────┐
                         │   FRONTEND APP   │
                         │  (Web/Mobile)    │
                         └────────┬─────────┘
                                  │
                    HTTP/HTTPS REST API Requests
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
              ┌──────────────┐          ┌──────────────┐
              │  AUTH ROUTES │          │  FOOD ROUTES │
              │              │          │              │
              ├─ /register   │          ├─ GET /foods/ │
              ├─ /verify     │          ├─ GET /cats   │
              ├─ /login      │          └─ /foods/* *  │
              └──────────────┘          └──────────────┘
                    │                           │
                    │     ┌──────────────┐     │
                    │     │ CART ROUTES  │     │
                    │     │              │     │
                    │     ├─ GET /cart/  │     │
                    │     ├─ POST /cart/ │     │
                    │     └─ DELETE /cart│     │
                    │     └──────────────┘     │
                    │            │             │
                    └────┬───────┴────┬────────┘
                         │            │
                         │            ▼ (Orders)
                         │      ┌──────────────┐
                         │      │ORDER ROUTES  │
                         │      │              │
                         │      ├─ GET /orders │
                         │      ├─ POST /orders│
                         │      └─ /orders/*   │
                         │      └──────────────┘
                         │            │
                         ▼            ▼
                    ┌─────────────────────────┐
                    │  FASTAPI APPLICATION   │
                    │                         │
                    │  - Request validation   │
                    │  - Authentication      │
                    │  - Business logic      │
                    │  - Session management  │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴───────────┐
                    │                        │
                    ▼                        ▼
            ┌──────────────────┐    ┌──────────────────┐
            │   SQLALCHEMY     │    │  SESSION STORAGE │
            │   SERVICE LAYER  │    │  (Cookie-based)  │
            │                  │    │                  │
            │ - auth_service   │    │ - Cart items     │
            │ - food_service   │    │ - User session   │
            │ - order_service  │    │ - Timestamps     │
            └────────┬─────────┘    └──────────────────┘
                     │
                     ▼
            ┌──────────────────┐
            │  SQLITE DATABASE │
            │                  │
            │ Tables:          │
            │ - users          │
            │ - foods          │
            │ - categories     │
            │ - orders         │
            │ - order_items    │
            └──────────────────┘
```
