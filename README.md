# FinBudPlanner

A personal finance management application with Angular frontend and FastAPI backend.

## Project Structure

```
FinBudPlanner/
├── backend/          # FastAPI backend with SQLite database
├── frontend/         # Angular frontend application
├── database/         # SQLite database file (auto-created)
├── start.py          # Python script to start both servers
└── start.sh          # Bash script to start both servers
```

## Quick Start

### Option 1: Python Script (Cross-platform)

```bash
python start.py
```

### Option 2: Bash Script (Linux/Mac)

```bash
./start.sh
```

### Option 3: Manual Start

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set SECRET_KEY
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## Access Points

- **Frontend:** http://localhost:4200
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Setup Requirements

### Backend
- Python 3.8+
- pip
- SECRET_KEY in `backend/.env` (copy from `.env.example`)

### Frontend
- Node.js 16+
- npm

## User Registration

When you first run the application, you'll need to register an account:

**Username Requirements:**
- At least 3 characters
- Must start with a letter
- Only letters, numbers, and underscores

**Password Requirements:**
- At least 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

## Features

- 💰 Income tracking
- 💸 Expense logging
- 📊 Budget management by category
- 📈 Dashboard with financial summaries
- 📉 Visual progress indicators for budget limits
- 🔐 Secure authentication with JWT tokens

## Development

### Backend Development
```bash
cd backend
# Install dependencies
pip install -r requirements.txt
# Run tests (if available)
pytest
# Start backend only
python main.py
```

### Frontend Development
```bash
cd frontend
# Install dependencies
npm install
# Start frontend only
npm start
# Build for production
ng build --configuration production
```

## Database

The SQLite database is automatically created at `database/finbud.db` when the backend first starts.

## Security Notes

- Never commit the `.env` file to version control
- Use strong, randomly generated SECRET_KEY in production
- Passwords are hashed using bcrypt
- All API endpoints (except register/login) require JWT authentication
