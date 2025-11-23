# E-Commerce Platform

A modern full-stack e-commerce platform built with Next.js, FastAPI, and MongoDB.

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Axios** - HTTP client

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **JWT** - Authentication
- **Passlib** - Password hashing

## Project Structure

```
ECOMMERCE-APP/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py
│   │   │       │   ├── users.py
│   │   │       │   ├── products.py
│   │   │       │   ├── cart.py
│   │   │       │   ├── orders.py
│   │   │       │   └── admin.py
│   │   │       └── api.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── cart.py
│   │   │   └── order.py
│   │   └── schemas/
│   │       ├── auth.py
│   │       ├── user.py
│   │       ├── product.py
│   │       ├── cart.py
│   │       └── order.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── layout.tsx
    │   │   ├── page.tsx
    │   │   └── globals.css
    │   ├── lib/
    │   │   └── api.ts
    │   ├── store/
    │   │   ├── authStore.ts
    │   │   └── cartStore.ts
    │   └── types/
    │       └── index.ts
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.ts
    └── next.config.js
```

## Features

### User Features
- ✅ User registration and authentication
- ✅ JWT-based authorization
- ✅ User profile management
- ✅ Product browsing with filters and search
- ✅ Shopping cart functionality
- ✅ Order placement and tracking
- ✅ Order history

### Admin Features
- ✅ Product management (CRUD)
- ✅ Order management
- ✅ User management
- ✅ Dashboard analytics

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/forgot-password` - Request password reset
- `POST /api/v1/auth/reset-password` - Reset password

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update profile
- `GET /api/v1/users/{user_id}` - Get user by ID

### Products
- `GET /api/v1/products` - List products (with filters)
- `GET /api/v1/products/{product_id}` - Get product details
- `GET /api/v1/products/category/{category}` - Get by category
- `GET /api/v1/products/search/{query}` - Search products

### Cart
- `GET /api/v1/cart` - Get user's cart
- `POST /api/v1/cart/items` - Add item to cart
- `PUT /api/v1/cart/items/{item_id}` - Update cart item
- `DELETE /api/v1/cart/items/{item_id}` - Remove from cart
- `DELETE /api/v1/cart` - Clear cart

### Orders
- `POST /api/v1/orders` - Create order
- `GET /api/v1/orders` - Get user's orders
- `GET /api/v1/orders/{order_id}` - Get order details
- `PUT /api/v1/orders/{order_id}/cancel` - Cancel order
- `GET /api/v1/orders/{order_id}/status` - Get order status

### Admin
- `POST /api/v1/admin/products` - Create product
- `PUT /api/v1/admin/products/{product_id}` - Update product
- `DELETE /api/v1/admin/products/{product_id}` - Delete product
- `GET /api/v1/admin/orders` - Get all orders
- `PUT /api/v1/admin/orders/{order_id}/status` - Update order status
- `GET /api/v1/admin/users` - Get all users
- `DELETE /api/v1/admin/users/{user_id}` - Delete user
- `GET /api/v1/admin/analytics/dashboard` - Dashboard analytics

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
copy .env.example .env
```

5. Update `.env` with your configuration

6. Run the server:
```bash
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```bash
copy .env.local.example .env.local
```

4. Run development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Development

- Backend runs on port 8000
- Frontend runs on port 3000
- MongoDB default port 27017

## Next Steps

1. Implement authentication endpoints
2. Add product management
3. Implement cart functionality
4. Build order processing
5. Create frontend pages and components
6. Add payment integration
7. Implement email notifications
8. Add unit tests

## License

MIT