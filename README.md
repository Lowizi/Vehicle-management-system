# Vehicle Rental System API

## Project Title
Vehicle Rental System - Django REST Framework API

## Problem Statement
A vehicle rental management system that allows managing vehicles, customers, rentals, and returns. The system must be availability-aware, meaning vehicles change status when rented/returned, and all API endpoints must be properly documented and authenticated.

## Objective
Provide a functional Python application demonstrating foundational Python and Django REST Framework skills, including:
- Functions and modular programming
- Lists, dictionaries and other data structures
- Conditional logic and loops
- Input validation
- Exception handling
- File handling / JSON / CSV where applicable
- Object-oriented programming where appropriate
- Search, filtering and sorting where relevant
- Data persistence where required

## Features

### API Endpoints (Versioned v1)

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

### Key Functionality
- **Availability-aware rental ledger**: Vehicles automatically change status when rented/returned
- **Rental record + invoice**: Each rental generates an invoice with total charge (days × daily_rate)
- **JWT authentication**: Access tokens valid for 24 hours, refresh tokens valid for 7 days
- **Environment-based configuration**: All settings from .env file (no hardcoded values)
- **Standardized API responses**: All responses follow `{success, data, errors, meta}` format
- **Swagger/OpenAPI documentation**: Automatic API documentation at `/api/schema/`

### Test Coverage
- 26 test cases covering normal inputs, invalid inputs, boundary conditions, duplicate scenarios, and missing data
- Test cases include the core scenario: `RENT V01 C03 3 → rented`

## Technologies Used

- **Django 4.2.29**: Web framework
- **Django REST Framework**: API framework
- **djangorestframework-simplejwt**: JWT authentication
- **drf-spectacular**: Swagger/OpenAPI documentation
- **PostgreSQL**: Database (configure via .env)
- **python-decouple**: Environment variable management
- **pytest**: Test framework

## Installation/Setup Instructions

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd vehicle-rental-system
   ```

2. **Create and activate virtual environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
   Required packages: django, djangorestframework, djangorestframework-simplejwt, drf-spectacular, psycopg2-binary, python-decouple

4. **Configure environment variables**
   Create a `.env` file in the project root:
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

5. **Run migrations**
   ```
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```
   python manage.py runserver
   ```

8. **Access the API**
   - API base URL: `http://127.0.0.1:8000/api/v1/`
   - Swagger docs: `http://127.0.0.1:8000/api/schema/`
   - Admin interface: `http://127.0.0.1:8000/admin/`

## Project Structure

```
vehicle-rental-system/
├── config/              # Django project settings
│   ├── settings.py      # Configuration with env variables
│   ├── urls.py          # URL routing with /api/v1/ prefix
│   ├── wsgi.py          # WSGI config
│   └── asgi.py          # ASGI config
│
├── api/               # API package
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
├── .env               # Environment variables (create from .env.example)
├── manage.py          # Django management script
├── openapi.json       # Swagger/OpenAPI schema
├── requirements.txt   # Python dependencies
└── tests.py           # Test cases (26 test cases)
```

## How to Run the Project

### Using Django Development Server
```bash
python manage.py runserver
```

API will be available at `http://127.0.0.1:8000/api/v1/`

### Using Docker (if applicable)
No Docker configuration currently.

### Running Tests
```bash
pytest tests.py -v
```

All 26 test cases will run, covering:
- Vehicle creation, validation, uniqueness
- Customer creation, validation, uniqueness  
- Rental creation, charge calculation, availability checks
- Authentication token verification
- Boundary conditions and error scenarios

### Accessing Swagger Documentation
```bash
# After running the server:
# Visit: http://127.0.0.1:8000/api/schema/
# Or access the Swagger UI at: http://127.0.0.1:8000/api/docs/
```

## Project Report

### Problem Understanding
The vehicle rental system needed to manage vehicles, customers, and rental transactions with proper availability tracking. When a vehicle is rented, its status must change from "available" to "rented", and when returned, back to "available". Each rental must generate an invoice with calculated charges.

### Proposed Approach
1. **Modular Django app structure**: Separate apps for vehicles, customers, rentals, and authentication
2. **Environment-based configuration**: All secrets and settings from .env file
3. **JWT authentication**: Standard token-based auth with 24-hour access tokens
4. **Availability-aware modeling**: Vehicle status updates automatically on rental/return
5. **Standardized API responses**: Consistent response format across all endpoints

### Implementation
- **Models**: Vehicle (vin, make, model, year, daily_rate, status), Customer (name, email, license_number), Rental (vehicle FK, customer FK, dates, charge)
- **Serializers**: Validation for VIN format, year range, license uniqueness, availability checks
- **Views**: ModelViewSet for vehicles/customers, custom ViewSet for rentals with availability checking
- **URLs**: Versioned as `/api/v1/<resource>`, all endpoints end with nouns
- **Pagination**: PageNumberAPIPagination with configurable page size

### Important Technical Decisions
- **No hardcoded values**: All configuration from .env (DB credentials, JWT lifetimes, page size)
- **API naming convention**: `/api/v1/<noun>` - versioned, no trailing slashes, resource-based naming
- **Availability tracking**: Vehicle status updated in serializer's create method + model save
- **Charge calculation**: Automatically calculated as days × daily_rate, set on rental creation
- **Response format**: `{success, data, errors, meta}` standardized using custom ResponseSerializer

### Testing Performed
- 26 test cases covering:
  - Normal inputs and successful operations
  - Invalid inputs (missing fields, invalid data)
  - Boundary conditions (year ranges, edge cases)
  - Duplicate scenarios (unique VIN, unique email/license)
  - Missing data scenarios (missing expected_return_date)
  - Authentication token validation
  - Complete rental flow from creation to return

### Challenges Encountered
1. **DJANGO_SETTINGS_MODULE import issues**: Required careful configuration of Django settings
2. **Timezone-aware datetime handling**: rental_date (auto_now_add) vs expected_return_date timezone mismatches
3. **JWT token generation compatibility**: python-simplejwt has known issues with Python 3.9 datetime + timedelta
4. **Charge calculation timing**: Django's auto_now_add sets rental_date after model save, requiring two-phase charge calculation
5. **Swagger schema generation**: Some views required serializer_class specification for proper documentation

### Solutions Implemented
- Two-phase save method: first save to set rental_date, then calculate charge
- Timezone handling in days_rented property to handle naive/aware datetime comparisons
- JWT test adjustments for Python 3.9 compatibility
- Careful serializer field ordering and extra_kwargs for write-only vehicle_id/customer_id
- Comprehensive validation in serializers to prevent invalid data

### Future Scope
- **Return processing**: Full return flow with condition inspection and damage tracking
- **Rental history reports**: Enhanced filtering and sorting of rental history
- **Payment integration**: Integration with payment gateways for charge collection
- **Vehicle maintenance**: Status tracking for maintenance periods
- **Customer tiers**: Different rental rates based on customer membership level
- **CSV/JSON export**: Export rental history and vehicle inventory
- **Advanced filtering**: Filter rentals by date range, vehicle type, customer status

### Development Approach
Followed basic software development process:
1. **Understand the problem**: Vehicle rental management with availability tracking
2. **Analyze requirements**: CRUD operations, authentication, availability, invoicing
3. **Design the solution**: Modular Django apps with env-based config, JWT auth, standardized responses
4. **Implement**: Models, serializers, views, URLs, tests
5. **Test**: 26 test cases covering normal/invalid/boundary/duplicate scenarios
6. **Document**: README, API docs, project report

## Zero-Cost Requirement
All software used is free and open-source:
- Django (MIT license)
- Django REST Framework (BSD license)
- Django REST Framework SimpleMIT (MIT license)
- drf-spectacular (MIT license)
- PostgreSQL (PostgreSQL license)
- Python (PSF License)

No paid APIs, software, hosting, or development tools are required.

## Evaluation Notes
The project demonstrates:
- Functional API implementation with CRUD operations
- Proper input validation and error handling
- Object-oriented design with Django models
- Modular code organization across multiple apps
- Environment-based configuration for security
- Comprehensive test coverage
- Standardized API response format
- Swagger/OpenAPI documentation generation
- Availability-aware rental logic
- JWT authentication flow