# Project Documentation: Vehicle Rental Systems API

## Overview
Vehicle Rental Systems is a Django REST Framework API for managing vehicle rentals, customers, and rental transactions. The system is availability-aware, meaning vehicle statuses automatically update when vehicles are rented or returned.

## Project Structure

```
vehicle-rental-system/
├── config/              # Django project settings
│   ├── settings.py      # Configuration with env variables
│   ├── urls.py          # URL routing with /api/v1/ prefix
│   ├── wsgi.py          # WSGI config
│   └── asgi.py          # ASGI config
│
├── api/                 # API package
│   ├── __init__.py
│   ├── responses.py     # Standardized response serializer
│   ├── pagination.py    # Custom pagination class
│   │
│   ├── vehicles/        # Vehicle module
│   │   ├── models.py    # Vehicle model with status tracking
│   │   ├── serializers.py # Vehicle serializer with validation
│   │   ├── views.py     # Vehicle CRUD views
│   │   └── urls.py      # Vehicle URLs
│   │
│   ├── customers/       # Customer module
│   │   ├── models.py    # Customer model
│   │   ├── serializers.py # Customer serializer
│   │   ├── views.py     # Customer CRUD views
│   │   └── urls.py      # Customer URLs
│   │
│   ├── rentals/         # Rental module
│   │   ├── models.py    # Rental model with charge calculation
│   │   ├── serializers.py # Rental serializer with availability check
│   │   ├── views.py     # Rental CRUD views
│   │   └── urls.py      # Rental URLs
│   │
│   └── authentication/  # Auth module
│       ├── models.py    # User session tokens
│       ├── serializers.py # User serializer
│       ├── views.py     # Login + token verify views
│       └── urls.py      # Auth URLs
│
├── .env                 # Environment variables
├── manage.py            # Django management script
├── openapi.json         # Swagger/OpenAPI schema
├── requirements.txt     # Python dependencies
└── tests.py             # Test cases (26 test cases)
```

## API Endpoints (Versioned v1)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/vehicles` | GET/POST | Bearer | List/create vehicles with availability status |
| `/api/v1/vehicles/{id}` | GET/PATCH/DELETE | Bearer | View/update/delete specific vehicle |
| `/api/v1/customers` | GET/POST | Bearer | List/create customers |
| `/api/v1/customers/{id}` | GET/PATCH/DELETE | Bearer | View/update/delete specific customer |
| `/api/v1/rentals` | GET/POST | Bearer | Customer rental history/create new rental |
| `/api/v1/auth/login` | POST | None | JWT token issuance (username/password) |
| `/api/v1/auth/verify` | GET | Bearer | Token validity verification |
| `/api/schema/` | GET | None | OpenAPI schema JSON |
| `/api/schema/swagger-ui/` | GET | None | Swagger UI documentation |
| `/api/schema/redoc/` | GET | None | ReDoc documentation |

## Key Features

- **Availability-aware rental ledger**: Vehicles automatically change status from "available" to "rented" when rented, and back to "available" when returned
- **Rental record + invoice**: Each rental generates an invoice with total charge (days × daily_rate)
- **JWT authentication**: Access tokens valid for 24 hours, refresh tokens valid for 7 days
- **Environment-based configuration**: All settings from .env file (no hardcoded values)
- **Standardized API responses**: All responses follow `{success, data, errors, meta}` format
- **Swagger/OpenAPI documentation**: Automatic API documentation at `/api/schema/`

## Technologies Used

- **Django 4.2.29**: Web framework
- **Django REST Framework**: API framework
- **djangorestframework-simplejwt**: JWT authentication
- **drf-spectacular**: Swagger/OpenAPI documentation
- **PostgreSQL**: Database (configure via .env)
- **python-decouple**: Environment variable management
- **pytest**: Test framework

## API Functionality

### Vehicles
- List and create vehicles
- Each vehicle has VIN, make, model, year, daily_rate, and status (available/rented)
- Status automatically updates when vehicles are rented/returned
- Validation for VIN format and year range

### Customers
- List and create customers
- Each customer has name, email, and license number
- License number must be unique

### Rentals
- Create new rentals with availability checking
- Charge calculated automatically as (days × daily_rate)
- Optional customer_id query parameter for filtering rental history
- Rental record includes rental_date (auto-generated) and expected_return_date

### Authentication
- Login with username/password returns JWT access/refresh tokens
- Token verification endpoint validates Bearer tokens
- No hardcoded credential values

## Response Format

All API responses follow a standardized format:
```json
{
  "success": true,
  "data": { ... },
  "errors": null,
  "meta": { ... }
}
```

## Configuration

All configuration is environment-based via the `.env` file:

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DB_NAME=vehicle-system
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
PAGE_SIZE=20
JWT_ACCESS_LIFETIME_HOURS=24
JWT_REFRESH_LIFETIME_DAYS=7
THROTTLE_RATE=20/min
```

## Testing

- **26 test cases** covering:
  - Normal inputs and successful operations
  - Invalid inputs (missing fields, invalid data)
  - Boundary conditions (year ranges, edge cases)
  - Duplicate scenarios (unique VIN, unique email/license)
  - Missing data scenarios
  - Authentication token validation
  - Complete rental flow from creation to return

Run tests with: `pytest tests.py -v`

## Swagger/OpenAPI Documentation

- **OpenAPI JSON**: `/api/schema/` - Generated by drf-spectacular
- **Swagger UI**: `/api/schema/swagger-ui/` - Interactive API documentation
- **ReDoc**: `/api/schema/redoc/` - Alternative API documentation

Documentation includes all models, security schemes, and operation endpoints with request/response details.

## Deployment Steps

1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment variables in `.env` file
5. Run migrations: `python manage.py migrate`
6. Create superuser (optional): `python manage.py createsuperuser`
7. Run development server: `python manage.py runserver`
8. API available at: `http://127.0.0.1:8000/api/v1/`
9. Swagger docs at: `http://127.0.0.1:8000/api/schema/swagger-ui/`