# FinBudPlanner Backend

FastAPI backend with SQLite database for FinBudPlanner application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set a strong SECRET_KEY
# You can generate one using: python -c "import secrets; print(secrets.token_urlsafe(32))"
```

3. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database

The SQLite database will be automatically created at `../database/finbud.db` on first run.

## User Registration Requirements

### Username Requirements:
- At least 3 characters long
- Must start with a letter
- Can only contain letters, numbers, and underscores
- Example: `john_doe123`

### Password Requirements:
- At least 8 characters long
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (!@#$%^&*(),.?":{}|<>)
- Example: `SecurePass123!`

## API Endpoints

### Authentication
- `POST /api/register` - Register new user (requires valid username and password)
- `POST /api/token` - Login with existing credentials (get JWT token)
- `GET /api/users/me` - Get current user info

### Income
- `POST /api/income` - Create income record
- `GET /api/income` - Get all income records
- `GET /api/income/{id}` - Get specific income record
- `DELETE /api/income/{id}` - Delete income record

### Expenses
- `POST /api/expense` - Create expense record
- `GET /api/expense` - Get all expense records
- `GET /api/expense/{id}` - Get specific expense record
- `DELETE /api/expense/{id}` - Delete expense record

### Budgets
- `POST /api/budget` - Create budget
- `GET /api/budget` - Get all budgets (with spending)
- `GET /api/budget/{id}` - Get specific budget (with spending)
- `DELETE /api/budget/{id}` - Delete budget

### Dashboard
- `GET /api/dashboard/summary` - Get financial summary
- `GET /api/dashboard/expenses-by-category` - Get expenses by category
- `GET /api/dashboard/recent-transactions` - Get recent transactions

## Authentication

All endpoints (except `/api/register` and `/api/token`) require JWT authentication.

Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Security Notes

- The `SECRET_KEY` in `.env` must be set before running the application
- Use a strong, randomly generated secret key in production
- Never commit the `.env` file to version control
- Passwords are hashed using bcrypt before storage
