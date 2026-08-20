# Vehicle Rental Systems: How It Works

## What This Project Does

Vehicle Rental Systems is a Django REST API that manages vehicle rentals with **availability tracking**. When a vehicle is rented, its status automatically changes from "available" to "rented". When returned, it goes back to "available". Each rental generates an automatic invoice.

## The Rental Flow (Step by Step)

### 1. Authentication
- User logs in with username/password
- System returns JWT access token (valid 24 hours) and refresh token (valid 7 days)
- Token included as Bearer token in subsequent API calls

### 2. View Available Vehicles
- GET `/api/v1/vehicles` lists all vehicles with their current status
- Only available vehicles can be rented

### 3. Create a Rental (The Core Flow)
When a rental is created via POST `/api/v1/rentals`:

1. **Check availability** - System verifies the vehicle is currently "available"
2. **Create rental record** - Saves rental with:
   - Vehicle ID and customer ID
   - Rental date (auto-generated)
   - Expected return date (from request)
3. **Calculate charge** - Automatic calculation: `(days × daily_rate)`
   - Days computed from rental period
   - Charge stored on the rental record
4. **Update vehicle status** - Vehicle status changes from "available" to "rented"
5. **Return response** - Includes success flag, rental data, and total charge

### 4. Process Vehicle Return
- POST `/api/v1/returns` processes the return
- System updates vehicle status back to "available"
- Rental record marked as returned
- No additional charge calculation (one-time fee already applied at rental creation)

### 5. Rental History
- GET `/api/v1/rentals` lists all rentals
- Optional `?customer_id` query parameter to filter by customer
- Shows rental history with charges, dates, and vehicle/customer info

## Key Business Rules

| Rule | Description |
|------|-------------|
| **Availability-aware** | Vehicle status automatically updates on rent/return |
| **One charge per rental** | Charge calculated once at rental creation (days × daily_rate) |
| **No double-renting** | System prevents renting already-rented vehicles |
| **Automatic invoicing** | Total charge calculated and stored automatically |
| **JWT protected** | All rental operations require valid access token |

## Example: Renting a Vehicle

```
POST /api/v1/rentals
{
  "vehicle": "vin-of-vehicle",
  "customer": "customer-id",
  "expected_return_date": "2024-01-15"
}
```

**What happens internally:**
```
✓ Validate vehicle exists and is available
✓ Calculate rental days from today to expected_return_date
✓ Charge = days × vehicle.daily_rate
✓ Create rental record with charge
✓ Update vehicle status: available → rented
✓ Return: {success: true, data: {rental, charge: $amount}}
```

## Example: Returning a Vehicle

```
POST /api/v1/returns
{
  "rental_id": "rental-uuid"
}
```

**What happens internally:**
```
✓ Find the rental record
✓ Update vehicle status: rented → available
✓ Mark rental as returned
✓ Return: {success: true, data: {message: "Vehicle returned"}}
```

## Technology Highlights

- **Django ORM** handles database operations and status updates
- **Atomic transactions** ensure rent/return operations are reliable
- **Timezone-aware datetime** handling for accurate day calculations
- **Serializer-level validation** prevents invalid rental operations
- **Standardized responses** consistent format across all endpoints