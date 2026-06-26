# Testing Guide for FinBudPlanner

This document explains the complete testing strategy for the FinBudPlanner application, including unit tests, integration tests, automated regression tests, performance tests, and CI/CD pipeline integration.

## Table of Contents

1. [Overview](#overview)
2. [Test Architecture](#test-architecture)
3. [Unit Tests](#unit-tests)
4. [Integration Tests](#integration-tests)
5. [Selenium Regression Tests](#selenium-regression-tests)
6. [JMeter Performance Tests](#jmeter-performance-tests)
7. [CI/CD Pipeline](#cicd-pipeline)
8. [Docker Testing](#docker-testing)
9. [Running Tests Locally](#running-tests-locally)
10. [Troubleshooting](#troubleshooting)

---

## Overview

FinBudPlanner employs a multi-layered testing approach to ensure application reliability and performance:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Selenium Tests**: End-to-end functional regression testing
- **JMeter Tests**: Performance and load testing
- **CI/CD Gatekeeper**: Automated testing pipeline that blocks failed builds

### Test Files Location

```
FinBudPlanner/
├── backend/
│   ├── Dockerfile                          # Backend container definition
│   ├── tests/
│   │   └── selenium_regression.py          # Selenium functional tests
│   └── requirements.txt                    # Python dependencies
├── frontend/
│   ├── Dockerfile                          # Frontend container definition
│   └── package.json                        # Node.js dependencies
├── database/
│   └── performance_profile.jmx            # JMeter performance test plan
└── .github/
    └── workflows/
        └── ci-gatekeeper.yml               # CI/CD pipeline configuration
```

---

## Test Architecture

### Testing Pyramid

```
                    /\
                   /  \
                  / E2E \        Selenium Tests (Functional)
                 /--------\
                /          \
               / Integration \   Docker Integration Tests
              /--------------\
             /                \
            /   Unit Tests     \  Pytest + Karma Tests
           /--------------------\
```

### CI/CD Pipeline Flow

```
┌─────────────┐
│  Push/PR    │
│  to main    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Stage 1:   │
│  Unit Tests  │  ← Python pytest + Angular Karma
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Stage 2:   │
│ Integration │  ← Build containers, start, verify
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Stage 3:   │
│  Automation  │  ← Selenium + JMeter
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Stage 4:   │
│   Push to   │  ← GHCR (only if all tests pass)
│    GHCR     │
└─────────────┘
```

---

## Unit Tests

### Backend Unit Tests

**Location**: `backend/tests/` (create test files here)

**Framework**: Python `unittest` and `pytest`

**How to Run**:
```bash
cd backend
pip install pytest
python -m pytest tests/ -v
```

**What to Test**:
- Model validation
- Business logic
- API endpoint responses (without database)
- Authentication logic

**Example Test Structure**:
```python
# backend/tests/test_models.py
import unittest
from models import Income

class TestIncomeModel(unittest.TestCase):
    def test_income_creation(self):
        income = Income(amount=1000, source="Salary")
        self.assertEqual(income.amount, 1000)
```

### Frontend Unit Tests

**Location**: `frontend/src/app/**/*..ts`

**Framework**: Angular Karma + Jasmine

**How to Run**:
```bash
cd frontend
npm install
npm run test -- --watch=false --browsers=ChromeHeadless
```

**What to Test**:
- Component logic
- Service methods
- Form validation
- Data transformation

**Example Test Structure**:
```typescript
// frontend/src/app/income/income.component..ts
describe('IncomeComponent', () => {
  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
```

---

## Integration Tests

### Docker Integration Tests

**Location**: `.github/workflows/ci-gatekeeper.yml` (Stage 2)

**What It Tests**:- Container build process
- Service startup
- Inter-service communication
- Health endpoint availability

**How It Works**:
1. Builds Docker images locally
2. Starts containers in detached mode
3. Waits for services to be ready
4. Verifies endpoints respond correctly

**Commands**:
```bash
# Build images
docker build -t finbud-backend:latest ./backend
docker build -t finbud-frontend:latest ./frontend

# Start containers
docker run -d -p 8000:8000 --name backend-test finbud-backend:latest
docker run -d -p 80:80 --name frontend-test finbud-frontend:latest

# Verify
curl -f http://localhost:8000/health
curl -f http://localhost:80
```

---

## Selenium Regression Tests

### File: `backend/tests/selenium_regression.py`

**Purpose**: End-to-end functional testing of the web application

**Framework**: Selenium WebDriver with Page Object Model (POM)

**Browser**: Chrome (headless mode for CI/CD)

### Test Structure

#### Page Object Model (POM)

The test suite uses the POM pattern for maintainability:

```python
LoginPage          # Encapsulates login page interactions
├── load()          # Navigate to login page
├── enter_username()
├── enter_password()
├── click_login()
└── is_loaded()

DashboardPage       # Encapsulates dashboard interactions
├── load()          # Navigate to dashboard
├── is_loaded()
└── get_username()
```

#### Test Cases

**Test 1: `test_user_login`**
- Navigates to login page
- Enters test credentials
- Submits login form
- Verifies redirect to dashboard
- Confirms dashboard loads successfully

**Test 2: `test_form_submission_workflow`**
- Logs into application
- Navigates to income page
- Opens add form
- Fills form fields
- Submits form
- Verifies form closes successfully

### Configuration

**Chrome Options for CI/CD**:
```python
chrome_options.add_argument('--headless=new')          # New headless mode
chrome_options.add_argument('--no-sandbox')             # Required for containers
chrome_options.add_argument('--disable-dev-shm-usage')  # Prevents memory issues
chrome_options.add_argument('--disable-gpu')            # No GPU needed
chrome_options.add_argument('--window-size=1920,1080') # Viewport size
```

### How to Run Locally

**Prerequisites**:
```bash
pip install selenium webdriver-manager
```

**Run Tests**:
```bash
cd backend
python tests/selenium_regression.py
```

**Run ific Test**:
```bash
python -m unittest tests.selenium_regression.SeleniumRegressionTests.test_user_login
```

### Test Data

**Default Credentials** (update these in the test file):
- Username: `testuser`
- Password: `testpass123`

### CI/CD Integration

The Selenium tests run in Stage 3 of the CI pipeline:

```yaml
- name: Install Selenium dependencies
  run: |
    pip install selenium webdriver-manager

- name: Run Selenium regression tests
  run: |
    cd backend
    python tests/selenium_regression.py
```

---

## JMeter Performance Tests

### File: `database/performance_profile.jmx`

**Purpose**: Load testing and performance benchmarking of the backend API

**Framework**: Apache JMeter 5.6.2

### Test Configuration

**Load Profile**:
- **Virtual Users**: 100 concurrent users
- **Ramp-up Time**: 60 seconds (gradually increase load)
- **Duration**: Single execution per user
- **Target Endpoint**: `http://localhost:8000/health`

**HTTP Request Configuration**:
```
Method: GET
Protocol: http
Host: ${__P(HOST,localhost)}  # Configurable via property
Port: ${__P(PORT,8000)}       # Configurable via property
Path: /health
```

**Assertions**:
- HTTP Response Code must be 200

**Listeners**:
- **View Results Tree**: Detailed request/response data
- **Summary Report**: Aggregated statistics (avg, min, max, throughput)

### How to Run Locally

**Install JMeter**:
```bash
# Ubuntu/Debian
sudo apt-get install jmeter

# macOS
brew install jmeter

# Or download from: https://jmeter.apache.org/download_jmeter.cgi
```

**Run Test**:
```bash
jmeter -n -t database/performance_profile.jmx -JHOST=localhost -JPORT=8000
```

**With Results File**:
```bash
jmeter -n -t database/performance_profile.jmx -JHOST=localhost -JPORT=8000 -l results.jtl
```

**View Results**:
```bash
jmeter -g results.jtl
```

### CI/CD Integration

The JMeter test runs in Stage 3 of the CI pipeline using the GitHub Action:

```yaml
- name: Run JMeter performance test
  uses: rlespinasse/github-action-jmeter@v3
  with:
    jmx-file: database/performance_profile.jmx
    args: -JHOST=localhost -JPORT=8000
```

### Performance Metrics

The test measures:
- **Response Time**: Time to receive response
- **Latency**: Time to first byte
- **Throughput**: Requests per second
- **Error Rate**: Percentage of failed requests
- **Connect Time**: Time to establish connection

---

## CI/CD Pipeline

### File: `.github/workflows/ci-gatekeeper.yml`

**Purpose**: Automated testing pipeline that acts as a gatekeeper for code quality

**Trigger Conditions**:
- Pull requests to `main` branch
- Direct pushes to `main` branch

### Pipeline Stages

#### Stage 1: Unit Tests

**Backend**:
```bash
cd backend
pip install -r requirements.txt
pip install pytest
python -m pytest tests/ -v
```

**Frontend**:
```bash
cd frontend
npm install
npm run test -- --watch=false --browsers=ChromeHeadless
```

**Failure Impact**: Pipeline stops, no further stages run

#### Stage 2: Integration & Local Stack

**Build Containers**:
```bash
docker build -t finbud-backend:latest ./backend
docker build -t finbud-frontend:latest ./frontend
```

**Start Services**:
```bash
docker run -d -p 8000:8000 --name backend-test finbud-backend:latest
docker run -d -p 80:80 --name frontend-test finbud-frontend:latest
```

**Verify Services**:
```bash
sleep 10
curl -f http://localhost:8000/health
curl -f http://localhost:80
```

**Failure Impact**: Pipeline stops, containers are cleaned up

#### Stage 3: Automation & Performance Engines

**Selenium Tests**:
```bash
pip install selenium webdriver-manager
cd backend
python tests/selenium_regression.py
```

**JMeter Tests**:
```yaml
- uses: rlespinasse/github-action-jmeter@v3
  with:
    jmx-file: database/performance_profile.jmx
    args: -JHOST=localhost -JPORT=8000
```

**Failure Impact**: Pipeline stops, containers are cleaned up

#### Stage 4: Registry Delivery

**Cleanup**:
```bash
docker stop backend-test frontend-test
docker rm backend-test frontend-test
```

**Login to GHCR**:
```yaml
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

**Push Images**:
```yaml
- uses: docker/build-push-action@v6
  with:
    context: ./backend
    file: ./backend/Dockerfile
    push: true
    tags: ghcr.io/${{ github.repository }}-backend:latest
```

**Success**: Images are pushed to GitHub Container Registry

### Gatekeeper Behavior

The pipeline implements a strict gatekeeper pattern:

- **Any test failure** → Pipeline stops, no images pushed
- **All tests pass** → Images pushed to GHCR
- **PR to main** → Tests must pass before merge can be completed
- **Push to main** → Tests run, images pushed on success

---

## Docker Testing

### Backend Dockerfile

**Location**: `backend/Dockerfile`

**Purpose**: Containerize the FastAPI backend

**Key Features**:
- Base: `python:3.11-slim`
- System dependencies: SQLite3 support
- Persistent database directory: `/app/database`
- Exposed port: 8000
- Environment variable: `DATABASE_PATH=/app/database/finbud.db`

**Build and Test**:
```bash
cd backend
docker build -t finbud-backend:test .
docker run -p 8000:8000 finbud-backend:test
curl http://localhost:8000/health
```

### Frontend Dockerfile

**Location**: `frontend/Dockerfile`

**Purpose**: Containerize the Angular frontend with multi-stage build

**Key Features**:
- **Stage 1 (Build)**: Node.js 20 for Angular compilation
- **Stage 2 (Serve)**: Nginx Alpine for static file serving
- Output directory: `dist/fin-bud-planner` (from angular.json)
- Exposed port: 80

**Build and Test**:
```bash
cd frontend
docker build -t finbud-frontend:test .
docker run -p 80:80 finbud-frontend:test
curl http://localhost:80
```

---

## Running Tests Locally

### Quick Test Run

```bash
# 1. Start backend
cd backend
source venv/bin/activate
python main.py

# 2. Start frontend (new terminal)
cd frontend
npm start

# 3. Run Selenium tests (new terminal)
cd backend
python tests/selenium_regression.py

# 4. Run JMeter test (new terminal)
jmeter -n -t database/performance_profile.jmx -JHOST=localhost -JPORT=8000
```

### Full CI Simulation

```bash
# Simulate CI pipeline locally
cd backend
pip install -r requirements.txt
pip install pytest
python -m pytest tests/ -v

cd ../frontend
npm install
npm run test -- --watch=false --browsers=ChromeHeadless

cd ..
docker build -t finbud-backend:latest ./backend
docker build -t finbud-frontend:latest ./frontend
docker run -d -p 8000:8000 --name backend-test finbud-backend:latest
docker run -d -p 80:80 --name frontend-test finbud-frontend:latest
sleep 10
curl -f http://localhost:8000/health
curl -f http://localhost:80

pip install selenium webdriver-manager
cd backend
python tests/selenium_regression.py

jmeter -n -t database/performance_profile.jmx -JHOST=localhost -JPORT=8000

docker stop backend-test frontend-test
docker rm backend-test frontend-test
```

---

## Troubleshooting

### Selenium Tests Fail

**Issue**: ChromeDriver not found
```bash
# Solution: Install webdriver-manager
pip install webdriver-manager
```

**Issue**: Element not found
```bash
# Solution: Increase wait time in WebDriverWait
# Or check if selectors match actual HTML
```

**Issue**: Headless mode issues
```bash
# Solution: Test with GUI mode first
# Remove --headless argument temporarily
```

### JMeter Tests Fail

**Issue**: Connection refused
```bash
# Solution: Ensure backend is running
curl http://localhost:8000/health
```

**Issue**: Port already in use
```bash
# Solution: Change PORT property
jmeter -n -t database/performance_profile.jmx -JPORT=8001
```

### Docker Tests Fail

**Issue**: Container won't start
```bash
# Solution: Check logs
docker logs backend-test
docker logs frontend-test
```

**Issue**: Port conflict
```bash
# Solution: Stop existing containers
docker stop backend-test frontend-test
docker rm backend-test frontend-test
```

### CI/CD Pipeline Fails

**Issue**: Tests pass locally but fail in CI
```bash
# Solution: Check CI logs for ific error
# Ensure all dependencies are in requirements.txt
# Verify Dockerfiles use correct paths
```

**Issue**: GHCR push fails
```bash
# Solution: Check repository permissions
# Ensure GitHub token has write access to packages
```

---

## Best Practices

1. **Write Tests First**: Test-driven development improves code quality
2. **Keep Tests Independent**: Each test should run in isolation
3. **Use Meaningful Names**: Test names should describe what they test
4. **Mock External Dependencies**: Don't rely on external services in unit tests
5. **Update Tests When Code Changes**: Keep tests in sync with production code
6. **Run Tests Locally Before Pushing**: Catch issues before CI
7. **Monitor Test Performance**: Slow tests slow down development
8. **Use Page Object Model**: Makes Selenium tests maintainable
9. **Version Pin Dependencies**: Ensure reproducible test runs
10. **Document Test Failures**: Add comments explaining why tests exist

---

## Summary

| Test Type | File | Framework | When It Runs | What It Tests |
|-----------|------|----------|--------------|---------------|
| Unit Tests | `backend/tests/*.py` | pytest | Every commit | Individual components |
| Unit Tests | `frontend/**/*..ts` | Karma/Jasmine | Every commit | Components/services |
| Integration | `ci-gatekeeper.yml` | Docker | Every commit | Container startup |
| Selenium | `backend/tests/selenium_regression.py` | Selenium | Every commit | E2E functionality |
| JMeter | `database/performance_profile.jmx` | JMeter | Every commit | API performance |
| CI/CD | `.github/workflows/ci-gatekeeper.yml` | GitHub Actions | PR/Push to main | All tests combined |

---

## Additional Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [JMeter User Manual](https://jmeter.apache.org/usermanual/index.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Angular Testing Guide](https://angular.io/guide/testing)
- [Pytest Documentation](https://docs.pytest.org/)
