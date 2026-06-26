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

### Option 2: Manual Start

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
- 🐳 Docker containerization support
- 🚀 CI/CD pipeline with automated testing
- 🧪 Selenium regression tests
- ⚡ JMeter performance testing

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

## Docker Deployment

### Build and Run with Docker Compose

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build

**Backend:**
```bash
cd backend
docker build -t finbud-backend:latest .
docker run -p 8000:8000 -v $(pwd)/../database:/app/database finbud-backend:latest
```

**Frontend:**
```bash
cd frontend
docker build -t finbud-frontend:latest .
docker run -p 80:80 finbud-frontend:latest
```

## CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline using GitHub Actions:

### Pipeline Stages

1. **Unit Tests**: Python unittest for backend, Angular Karma tests for frontend
2. **Integration Tests**: Build containers locally, launch them, and verify functionality
3. **Automation Tests**: Selenium regression tests using Page Object Model
4. **Performance Tests**: JMeter load testing with 100 concurrent users
5. **Registry Delivery**: Push images to GitHub Container Registry (GHCR)

### Trigger Conditions

- Pull requests to `main` branch
- Pushes to `main` branch

### Gatekeeper Behavior

The pipeline blocks merges to `main` if any test stage fails. Only successful runs push containers to GHCR.

### Test Files

- Selenium tests: `backend/tests/selenium_regression.py`
- JMeter profile: `database/performance_profile.jmx`
- CI workflow: `.github/workflows/ci-gatekeeper.yml`

## Database

The SQLite database is automatically created at `database/finbud.db` when the backend first starts.

## Security Notes

- Never commit the `.env` file to version control
- Use strong, randomly generated SECRET_KEY in production
- Passwords are hashed using bcrypt
- All API endpoints (except register/login) require JWT authentication
