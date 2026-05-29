# E-Commerce API

A production-ready REST API for an e-commerce platform — built with Django REST Framework. Features product catalog, shopping cart, and order management with JWT authentication.

## Features

- JWT Authentication (register, login, token refresh)
- Product catalog with categories, images, stock management
- Filter products by price range, category, stock availability
- Shopping cart (add, update quantity, remove items)
- Checkout flow with automatic stock deduction
- Order history per user
- Swagger UI auto-generated documentation
- Dockerized with PostgreSQL

## Tech Stack

- **Backend:** Python 3.11, Django 4.2, Django REST Framework
- **Database:** PostgreSQL 15
- **Auth:** JWT via `djangorestframework-simplejwt`
- **Docs:** Auto-generated Swagger via `drf-spectacular`
- **Media:** Pillow for product images
- **DevOps:** Docker, docker-compose

## Getting Started

### Prerequisites
- Docker & docker-compose installed

### Run locally

```bash
git clone https://github.com/your-username/ecommerce-api.git
cd ecommerce-api
cp .env.example .env
docker-compose up --build
```

API: `http://localhost:8000`  
Swagger docs: `http://localhost:8000/api/docs/`

### Setup

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Create account |
| POST | `/api/auth/login/` | Get JWT tokens |
| POST | `/api/auth/refresh/` | Refresh token |
| GET/PUT | `/api/auth/me/` | Profile |

### Store (public)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/store/products/` | List products |
| GET | `/api/store/products/{id}/` | Product detail |
| GET | `/api/store/products/featured/` | Featured products |
| GET | `/api/store/categories/` | List categories |

### Cart (auth required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/cart/` | View cart |
| POST | `/api/orders/cart/add/` | Add item to cart |
| PATCH | `/api/orders/cart/items/{id}/` | Update quantity |
| DELETE | `/api/orders/cart/items/{id}/` | Remove item |

### Orders (auth required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orders/checkout/` | Place order from cart |
| GET | `/api/orders/` | Order history |
| GET | `/api/orders/{id}/` | Order detail |

## Filtering & Search

```
# Filter by price range
GET /api/store/products/?min_price=10&max_price=100

# Filter by category
GET /api/store/products/?category=1

# Filter in-stock only
GET /api/store/products/?in_stock=true

# Search by name
GET /api/store/products/?search=shirt

# Order by price
GET /api/store/products/?ordering=price
```

## Example Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@test.com", "password": "pass1234", "password2": "pass1234"}'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "pass1234"}'

# 3. Add to cart
curl -X POST http://localhost:8000/api/orders/cart/add/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"product": 1, "quantity": 2}'

# 4. Checkout
curl -X POST http://localhost:8000/api/orders/checkout/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"shipping_address": "123 Main St, Lomé, Togo"}'
```

## License

MIT
