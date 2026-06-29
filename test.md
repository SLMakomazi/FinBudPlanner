# Testing Guide for FinBudPlanner

This document explains the complete testing strategy for the FinBudPlanner application, including unit tests, integration tests, automated regression tests, performance tests, and CI/CD pipeline integration.

**Last Updated**: June 29, 2026  
**Testing Architecture Refactored**: Enterprise-grade testing framework with Allure reporting, Page Object Model, and comprehensive test coverage

## Table of Contents

1. [Overview](#overview)
2. [Test Architecture](#test-architecture)
3. [Backend Unit Tests](#backend-unit-tests)
4. [Backend Integration Tests](#backend-integration-tests)
5. [Selenium E2E Tests](#selenium-e2e-tests)
6. [Angular Component Tests](#angular-component-tests)
7. [JMeter Performance Tests](#jmeter-performance-tests)
8. [Allure Reporting](#allure-reporting)
9. [CI/CD Pipeline](#cicd-pipeline)
10. [Docker Testing](#docker-testing)
11. [Running Tests Locally](#running-tests-locally)
12. [Troubleshooting](#troubleshooting)

---

## Overview

FinBudPlanner employs a multi-layered testing approach to ensure application reliability and performance:

- **Backend Unit Tests**: Test individual API endpoints, validation, error handling, and edge cases
- **Backend Integration Tests**: Test component interactions with database
- **Selenium E2E Tests**: End-to-end functional regression testing with Page Object Model
- **Angular Component Tests**: Test frontend components with Jasmine/Karma
- **JMeter Tests**: Performance and load testing
- **CI/CD Gatekeeper**: Automated testing pipeline that blocks failed builds
- **Allure Reporting**: Comprehensive test reporting with hierarchy and attachments

### Test Files Location

```
FinBudPlanner/
├── backend/
│   ├── pytest.ini                          # Pytest configuration with markers and coverage
│   ├── requirements.txt                    # Python dependencies (includes pytest, allure, selenium)
│   ├── tests/
│   │   ├── conftest.py                     # Shared pytest fixtures
│   │   ├── unit/                           # Unit tests (validation, edge cases, error handling)
│   │   │   ├── test_auth_unit.py          # Authentication unit tests (15 tests)
│   │   │   ├── test_budget_unit.py        # Budget unit tests (18 tests)
│   │   │   ├── test_income_unit.py        # Income unit tests (18 tests)
│   │   │   ├── test_expense_unit.py       # Expense unit tests (18 tests)
│   │   │   ├── test_dashboard_unit.py     # Dashboard unit tests (8 tests)
│   │   │   ├── test_users_unit.py         # User management unit tests (5 tests)
│   │   │   └── test_health_unit.py        # Health endpoint unit tests (6 tests)
│   │   ├── integration/                    # Integration tests (with database)
│   │   │   ├── test_auth.py               # Authentication integration tests
│   │   │   ├── test_budget.py             # Budget integration tests
│   │   │   ├── test_income.py             # Income integration tests
│   │   │   ├── test_expense.py            # Expense integration tests
│   │   │   ├── test_dashboard.py          # Dashboard integration tests
│   │   │   ├── test_users.py              # User integration tests
│   │   │   └── test_health.py             # Health integration tests
│   │   └── selenium/                       # Selenium E2E tests with Page Object Model
│   │       ├── pages/                      # Page Object Model classes
│   │       │   ├── base_page.py           # Base page with common functionality
│   │       │   ├── login_page.py          # Login page object
│   │       │   ├── signup_page.py         # Signup page object
│   │       │   └── dashboard_page.py      # Dashboard page object
│   │       ├── helpers/                    # Reusable Selenium helpers
│   │       │   └── selenium_helpers.py    # Helper methods for common operations
│   │       ├── test_selenium_login.py     # Login workflow test
│   │       └── test_selenium_income.py    # Income workflow test
│   └── Dockerfile                          # Backend container definition
├── frontend/
│   ├── src/app/
│   │   ├── login/
│   │   │   └── login.component.spec.ts    # Login component tests (8 tests)
│   │   ├── signup/
│   │   │   └── signup.component.spec.ts   # Signup component tests (11 tests)
│   │   ├── income/
│   │   │   └── income.component.spec.ts   # Income component tests (13 tests)
│   │   ├── expense/
│   │   │   └── expense.component.spec.ts  # Expense component tests (13 tests)
│   │   ├── budget/
│   │   │   └── budget.component.spec.ts   # Budget component tests (13 tests)
│   │   ├── dashboard/
│   │   │   └── dashboard.component.spec.ts # Dashboard component tests (20 tests)
│   │   └── app.component.spec.ts          # App component tests
│   ├── karma.conf.js                       # Karma test runner configuration
│   ├── package.json                        # Node.js dependencies
│   └── Dockerfile                          # Frontend container definition
├── database/
│   └── performance_profile.jmx            # JMeter performance test plan
└── .github/
    └── workflows/
        └── ci-gatekeeper.yml               # CI/CD pipeline configuration
```

### Test Coverage Summary

| Test Type | Count | Framework | Coverage Area |
|-----------|-------|-----------|---------------|
| Backend Unit Tests | 88 | pytest | Validation, authorization, error handling, CRUD, edge cases |
| Backend Integration Tests | 8 | pytest | API endpoint integration with database |
| Selenium E2E Tests | 2 | pytest + Selenium | User workflows with Page Object Model |
| Angular Component Tests | 78 | Jasmine/Karma | Component logic, validation, state management |
| JMeter Tests | 1 | Apache JMeter | API performance under load |
| **Total** | **177** | - | - |

---

## Test Architecture

### Testing Pyramid

```
                    /\
                   /  \
                  / E2E \        Selenium Tests (Functional)
                 /--------\        2 tests with Page Object Model
                /          \
               / Integration \   Integration Tests
              /--------------\    8 tests with database
             /                \
            /   Unit Tests     \  Unit Tests
           /--------------------\  88 backend + 78 frontend tests
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
│  Unit Tests  │  ← Backend unit + integration + Angular tests
│              │     Allure reporting enabled
└──────�──────┘
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
│              │     Automatic screenshots on failure
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Stage 4:   │
│   Reports   │  ← Allure + JMeter + Coverage reports
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Stage 5:   │
│   Push to   │  ← GHCR (only if all tests pass)
│    GHCR     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Stage 6:   │
│  Deploy to  │  ← GitHub Pages (Allure reports)
│  GitHub     │
│   Pages     │
└─────────────┘
```

### Allure Report Hierarchy

```
Backend API
├── Authentication
│   ├── User Registration
│   │   └── Successful user registration
│   │   └── Registration with duplicate username
│   │   └── Registration with invalid password
│   └── User Login
│       └── Successful user login
│       └── Login with invalid credentials
├── Budget
│   ├── Budget Management
│   │   ├── Create Budget
│   │   ├── Get Budgets
│   │   ├── Update Budget
│   │   └── Delete Budget
├── Income
├── Expense
├── Dashboard
├── Users
└── Health

Frontend UI
└── Selenium UI
    ├── User Authentication
    │   └── User Login
    └── Income Management
        └── Income Workflow
```

---

## Backend Unit Tests

**Location**: `backend/tests/unit/`

**Framework**: Python `pytest` with Allure reporting

**Configuration**: `backend/pytest.ini`

### Test Files

#### test_auth_unit.py (15 tests)
Tests authentication validation and error handling:
- Successful user registration
- Registration with duplicate username
- Registration with invalid password (too short, no special char)
- Registration with missing fields
- Registration with empty fields
- Successful user login
- Login with invalid username
- Login with invalid password
- Login with missing credentials
- Login with empty credentials

#### test_budget_unit.py (18 tests)
Tests budget CRUD operations and validation:
- Create budget with valid data
- Create budget with missing category/limit
- Create budget with negative/zero limit
- Create budget without authentication
- Get all budgets
- Get budgets without authentication
- Get budgets for new user (empty list)
- Update budget successfully
- Update budget with invalid ID
- Update budget without authentication
- Delete budget successfully
- Delete budget with invalid ID
- Delete budget without authentication

#### test_income_unit.py (18 tests)
Tests income CRUD operations and validation:
- Create income with valid data
- Create income with missing fields
- Create income with negative/zero amount
- Create income with invalid date format
- Create income without authentication
- Get all income records
- Get income without authentication
- Get income for new user (empty list)
- Update income successfully
- Update income with invalid ID
- Update income without authentication
- Delete income successfully
- Delete income with invalid ID
- Delete income without authentication

#### test_expense_unit.py (18 tests)
Tests expense CRUD operations and validation (similar structure to income)

#### test_dashboard_unit.py (8 tests)
Tests dashboard functionality:
- Get dashboard summary successfully
- Get dashboard summary without authentication
- Dashboard summary returns numeric values
- Get recent transactions successfully
- Get recent transactions without authentication
- Recent transactions returns empty list for new user
- Recent transactions with income and expense data

#### test_users_unit.py (5 tests)
Tests user management:
- Get current user successfully
- Get current user without authentication
- Get current user returns correct username
- User profile contains required fields
- User profile username is not empty

#### test_health_unit.py (6 tests)
Tests health endpoint:
- Health check returns 200 status
- Health check returns healthy status
- Health check response is JSON
- Health check response structure
- Health check does not require authentication

### How to Run

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest tests/unit -v --alluredir=allure-results --cov=. --cov-report=html --cov-report=term-missing
```

### Allure Decorators

All unit tests use Allure decorators for reporting:

```python
@allure.parent_suite("Backend API")
@allure.suite("Authentication")
@allure.feature("Authentication")
@allure.story("User Registration")
@allure.title("Successful user registration")
@allure.description("Verify that a new user can be registered with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
def test_register_success(self, test_client):
    # Test implementation
```

---

## Backend Integration Tests

**Location**: `backend/tests/integration/`

**Framework**: Python `pytest` with Allure reporting

### Test Files

All integration tests follow the same pattern with Allure decorators:

- `test_auth.py` - Authentication integration tests (register, login)
- `test_budget.py` - Budget integration tests (create, get)
- `test_income.py` - Income integration tests (create, get)
- `test_expense.py` - Expense integration tests (create, get)
- `test_dashboard.py` - Dashboard integration tests (summary, transactions)
- `test_users.py` - User integration tests (get current user)
- `test_health.py` - Health endpoint integration test

### How to Run

```bash
cd backend
pytest tests/integration -v --alluredir=allure-results
```

---

## Selenium E2E Tests

**Location**: `backend/tests/selenium/`

**Framework**: Selenium WebDriver with Page Object Model (POM) and pytest

### Page Object Model Structure

#### Base Page (`pages/base_page.py`)
Provides common functionality for all page objects:
- `navigate_to(url)` - Navigate to specific URL
- `get_current_url()` - Get current URL
- `get_title()` - Get page title
- `wait_for_page_load()` - Wait for page to load
- `is_loaded()` - Abstract method to be overridden

#### Login Page (`pages/login_page.py`)
Encapsulates login page interactions:
- `load()` - Navigate to login page
- `enter_username(username)` - Enter username
- `enter_password(password)` - Enter password
- `click_login()` - Click login button
- `login(username, password)` - Complete login action
- `is_loaded()` - Check if page is loaded
- `is_error_message_displayed()` - Check for error messages
- `get_error_message()` - Get error message text
- `click_login_here_link()` - Click login link

#### Signup Page (`pages/signup_page.py`)
Encapsulates signup page interactions:
- `load()` / `load_alternative()` - Navigate to signup page
- `enter_username(username)` - Enter username
- `enter_password(password)` - Enter password
- `enter_confirm_password(password)` - Enter confirm password
- `click_submit()` - Click submit button
- `signup(username, password)` - Complete signup action
- `is_loaded()` - Check if page is loaded
- `is_error_message_displayed()` - Check for error messages

#### Dashboard Page (`pages/dashboard_page.py`)
Encapsulates dashboard interactions:
- `load()` - Navigate to dashboard
- `is_loaded()` - Check if page is loaded
- `navigate_to_income()` - Navigate to income section
- `navigate_to_expense()` - Navigate to expense section
- `navigate_to_budget()` - Navigate to budget section
- `click_add_button()` - Click add button
- `is_form_displayed()` - Check if form is displayed
- `enter_source(source)` - Enter source
- `enter_amount(amount)` - Enter amount
- `enter_date(date)` - Enter date (using JavaScript for headless compatibility)
- `select_category(value)` - Select category from dropdown
- `submit_form()` - Submit form
- `wait_for_form_to_close()` - Wait for form to close
- `add_income(source, amount, date, category)` - Complete income workflow

### Selenium Helpers (`helpers/selenium_helpers.py`)

Reusable helper methods for common Selenium operations:
- `wait_for_element(locator, timeout)` - Wait for element presence
- `wait_for_element_clickable(locator, timeout)` - Wait for element to be clickable
- `wait_for_element_visible(locator, timeout)` - Wait for element visibility
- `wait_for_url_contains(text, timeout)` - Wait for URL to contain text
- `is_element_present(locator)` - Check if element is present
- `is_element_visible(locator)` - Check if element is visible
- `clear_and_send_keys(locator, text)` - Clear field and send keys
- `click_element(locator)` - Click on element
- `get_element_text(locator)` - Get text from element
- `take_screenshot(name)` - Take screenshot and attach to Allure
- `attach_browser_logs()` - Attach browser console logs to Allure
- `attach_page_source()` - Attach page source to Allure
- `attach_current_url()` - Attach current URL to Allure
- `capture_failure_artifacts(test_name)` - Capture all artifacts on test failure
- `select_dropdown_by_value(locator, value)` - Select dropdown by value
- `select_dropdown_by_visible_text(locator, text)` - Select dropdown by text
- `execute_script(script, *args)` - Execute JavaScript
- `scroll_to_element(locator)` - Scroll to element
- `wait_for_element_not_present(locator, timeout)` - Wait for element to not be present

### Test Files

#### test_selenium_login.py
Tests user login workflow with registration fallback:
- Logs in with test credentials
- Automatically registers user if not found
- Verifies dashboard loads after login
- Captures screenshots and logs on failure

#### test_selenium_income.py
Tests income creation workflow:
- Logs in to application
- Navigates to income section
- Opens add form
- Fills form fields
- Submits form
- Verifies form closes successfully
- Captures screenshots and logs on failure

### Automatic Failure Artifacts

On test failure, Selenium tests automatically capture:
- **Screenshot** - PNG image of the page at failure
- **Browser Console Logs** - JavaScript console errors and warnings
- **Page Source** - HTML source of the page at failure
- **Current URL** - URL where failure occurred

All artifacts are attached to Allure report for debugging.

### Configuration

**Chrome Options for CI/CD**:
```python
chrome_options.add_argument('--headless=new')          # New headless mode
chrome_options.add_argument('--no-sandbox')             # Required for containers
chrome_options.add_argument('--disable-dev-shm-usage')  # Prevents memory issues
chrome_options.add_argument('--disable-gpu')            # No GPU needed
chrome_options.add_argument('--window-size=1920,1080') # Viewport size
```

### How to Run

```bash
cd backend
pytest tests/selenium -v --alluredir=allure-results
```

**Run specific test**:
```bash
pytest tests/selenium/test_selenium_login.py::TestUserLogin::test_user_login -v
```

### Test Data

**Default Credentials** (update in test files):
- Username: `Siseko`
- Password: `Makomazi!1958`

---

## Angular Component Tests

**Location**: `frontend/src/app/**/*component.spec.ts`

**Framework**: Angular Karma + Jasmine

### Test Files

#### login.component.spec.ts (8 tests)
Tests login component:
- Component creation
- Username and password properties
- Error message initialization
- Loading state initialization
- Validation for missing fields
- Loading state on valid login
- Error message clearing on valid login

#### signup.component.spec.ts (11 tests)
Tests signup component:
- Component creation
- Username, password, confirmPassword properties
- Error and success message initialization
- Loading state initialization
- Validation for missing fields
- Password mismatch validation
- Loading state on valid signup
- Error message clearing on valid signup

#### income.component.spec.ts (13 tests)
Tests income component:
- Component creation
- Form state initialization
- Income list initialization
- New income object structure
- Default date setting
- Validation for missing fields
- Validation for invalid amount
- Total monthly income calculation
- Current month display
- Date formatting

#### expense.component.spec.ts (13 tests)
Tests expense component (similar structure to income)

#### budget.component.spec.ts (13 tests)
Tests budget component:
- Component creation
- Form state initialization
- Budget list initialization
- New budget object structure
- Validation for missing fields
- Validation for invalid limit
- Total budget calculation
- Total spent calculation
- Remaining budget calculation
- Progress percentage calculation
- Progress class determination (success/warning/danger)

#### dashboard.component.spec.ts (20 tests)
Tests dashboard component:
- Component creation
- Data structure initialization
- Selected tab initialization
- Total income calculation
- Total expenses calculation
- Net balance calculation
- Balance class determination
- Savings rate calculation
- Current month display
- Recent transactions sorting
- Tab selection
- Category formatting
- Date formatting
- Progress percentage calculation
- Progress class determination

### How to Run

```bash
cd frontend
npm install
npm test -- --configuration=ci
```

**Run specific test file**:
```bash
ng test --include='src/app/login/login.component.spec.ts'
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

## Allure Reporting

**Purpose**: Comprehensive test reporting with hierarchical organization, attachments, and history

**Framework**: Allure Test Report

### Configuration

**Backend pytest.ini**:
```ini
[pytest]
addopts = 
    -v
    --alluredir=allure-results
    --cov=.
    --cov-report=html
    --cov-report=term-missing
```

### Allure Decorators

All backend tests use Allure decorators for comprehensive reporting:

```python
@allure.parent_suite("Backend API")      # Top-level suite
@allure.suite("Authentication")          # Feature suite
@allure.feature("Authentication")        # Feature
@allure.story("User Registration")       # User story
@allure.title("Successful user registration")  # Test title
@allure.description("Verify that a new user can be registered with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)  # Severity
```

### Severity Levels

- **CRITICAL**: Core functionality that must work (authentication, CRUD operations)
- **HIGH**: Important features with workarounds available
- **MEDIUM**: Nice-to-have features
- **LOW**: Minor features

### Attachments

Tests automatically attach artifacts to Allure reports:

**Selenium Tests**:
- Screenshots on failure (PNG)
- Browser console logs (TEXT)
- Page source (TEXT)
- Current URL (TEXT)

**Backend Tests**:
- Request/response data can be attached manually
- Custom attachments for debugging

### Report Hierarchy

```
Backend API
├── Authentication
│   ├── User Registration
│   └── User Login
├── Budget
│   └── Budget Management
├── Income
│   └── Income Management
├── Expense
│   └── Expense Management
├── Dashboard
│   └── Dashboard Features
├── Users
│   └── User Management
└── Health
    └── Health Check

Frontend UI
└── Selenium UI
    ├── User Authentication
    └── Income Management
```

### Generating Reports

```bash
# Generate HTML report
allure generate allure-results -o allure-report

# Open report in browser
allure open

# Serve report on localhost
allure serve
```

### CI/CD Integration

Allure reports are automatically generated in CI/CD:
- Results collected in `backend/allure-results`
- Report generated using `simple-elf/allure-report-action`
- History preserved across runs
- Deployed to GitHub Pages

---

## CI/CD Pipeline

### File: `.github/workflows/ci-gatekeeper.yml`

**Purpose**: Automated testing pipeline that acts as a gatekeeper for code quality

**Trigger Conditions**:
- Pull requests to `main` branch
- Direct pushes to `main` branch

### Pipeline Stages

#### Stage 1: Unit Tests

**Backend Unit Tests**:
```bash
cd backend
pip install -r requirements.txt
pip install pytest selenium webdriver-manager allure-pytest pytest-cov
pytest tests/unit -v --alluredir=allure-results --cov=. --cov-report=html --cov-report=term-missing
```

**Backend Integration Tests**:
```bash
pytest tests/integration -v --alluredir=allure-results --cov=. --cov-report=html --cov-report=term-missing
```

**Frontend Tests**:
```bash
cd frontend
npm install
npm test -- --configuration=ci
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
cd backend
pytest tests/selenium -v --alluredir=allure-results
```

**JMeter Tests**:
```yaml
- uses: rlespinasse/github-action-jmeter@v3
  with:
    jmx-file: database/performance_profile.jmx
    args: -JHOST=localhost -JPORT=8000
```

**Failure Impact**: Pipeline stops, containers are cleaned up

#### Stage 4: Reports & Artifacts

**Upload Artifacts**:
- JMeter report: `jmeter-report/`
- Selenium Allure results: `backend/allure-results/`
- Backend coverage: `backend/coverage/`
- Combined reports: `all-reports.zip`

**Generate Allure Report**:
```yaml
- uses: simple-elf/allure-report-action@master
  with:
    allure_results: backend/allure-results
    allure_report: allure-report
    allure_history: allure-history
```

#### Stage 5: Registry Delivery

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

#### Stage 6: GitHub Pages Deployment

**Deploy Allure Reports**:
```yaml
- uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./allure-report
    publish_branch: gh-pages
```

**Success**: Allure reports deployed to GitHub Pages with history

### Gatekeeper Behavior

The pipeline implements a strict gatekeeper pattern:

- **Any test failure** → Pipeline stops, no images pushed
- **All tests pass** → Images pushed to GHCR, reports deployed to GitHub Pages
- **PR to main** → Tests must pass before merge can be completed
- **Push to main** → Tests run, images pushed on success
- **Report generation** → Allure reports always generated and uploaded, even on failure

### Updated Configuration

**Validation Step**:
```yaml
- name: Validate Required CI Inputs
  run: |
    test -n "${SECRET_KEY}"
    test -f backend/requirements.txt
    test -f backend/Dockerfile
    test -f backend/pytest.ini
    test -f backend/tests/selenium/test_selenium_login.py
    test -f backend/tests/selenium/test_selenium_income.py
    test -f frontend/package-lock.json
    test -f frontend/tsconfig.json
    test -f database/performance_profile.jmx
```

**Dependencies**:
```yaml
- name: Install Backend Dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install pytest selenium webdriver-manager allure-pytest pytest-cov
```

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

### Prerequisites

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend**:
```bash
cd frontend
npm install
```

### Backend Unit Tests

```bash
cd backend
pytest tests/unit -v --alluredir=allure-results --cov=. --cov-report=html --cov-report=term-missing
```

### Backend Integration Tests

```bash
cd backend
pytest tests/integration -v --alluredir=allure-results
```

### Selenium E2E Tests

**Prerequisites**: Backend and frontend must be running

```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
python main.py

# Terminal 2: Start frontend
cd frontend
npm start

# Terminal 3: Run Selenium tests
cd backend
pytest tests/selenium -v --alluredir=allure-results
```

### Angular Component Tests

```bash
cd frontend
npm test -- --configuration=ci
```

### All Backend Tests

```bash
cd backend
pytest tests/ -v --alluredir=allure-results --cov=. --cov-report=html
```

### Generate Allure Report

```bash
cd backend
allure generate allure-results -o allure-report
allure open
```

### Full CI Simulation

```bash
# Backend unit and integration tests
cd backend
pytest tests/unit tests/integration -v --alluredir=allure-results --cov=. --cov-report=html

# Frontend tests
cd ../frontend
npm test -- --configuration=ci

# Build containers
cd ..
docker build -t finbud-backend:latest ./backend
docker build -t finbud-frontend:latest ./frontend

# Start containers
docker run -d -p 8000:8000 --name backend-test finbud-backend:latest
docker run -d -p 80:80 --name frontend-test finbud-frontend:latest
sleep 10

# Verify services
curl -f http://localhost:8000/health
curl -f http://localhost:80

# Run Selenium tests
cd backend
pytest tests/selenium -v --alluredir=allure-results

# Run JMeter test
jmeter -n -t database/performance_profile.jmx -JHOST=localhost -JPORT=8000

# Cleanup
docker stop backend-test frontend-test
docker rm backend-test frontend-test

# Generate Allure report
allure generate allure-results -o allure-report
```

---

## Troubleshooting

### Backend Tests Fail

**Issue**: Module not found errors
```bash
# Solution: Ensure PYTHONPATH is set
export PYTHONPATH=.
# Or use pytest with PYTHONPATH
PYTHONPATH=. pytest tests/unit -v
```

**Issue**: Allure not found
```bash
# Solution: Install allure-commandline
# macOS
brew install allure

# Linux
sudo apt-get install allure

# Or download from: https://github.com/allure-framework/allure2/releases
```

### Selenium Tests Fail

**Issue**: ChromeDriver not found
```bash
# Solution: Install webdriver-manager (already in requirements.txt)
pip install webdriver-manager
```

**Issue**: Element not found
```bash
# Solution: Increase wait time in WebDriverWait
# Or check if selectors match actual HTML
# Use helper.capture_failure_artifacts() to debug
```

**Issue**: Headless mode issues
```bash
# Solution: Test with GUI mode first
# Remove --headless argument temporarily in test file
```

**Issue**: Frontend not accessible
```bash
# Solution: Ensure frontend is running on port 4200
# Check BASE_URL in test files
curl http://localhost:4200
```

### Angular Tests Fail

**Issue**: TypeScript errors in spec files
```bash
# Solution: These are IDE linting errors, not actual test failures
# Tests will run correctly with Karma/Jasmine
# Ignore these errors in IDE
```

**Issue**: Karma port already in use
```bash
# Solution: Change karma port in karma.conf.js
# Or kill existing karma process
lsof -ti:9876 | xargs kill
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
# Solution: Check CI logs for specific error
# Ensure all dependencies are in requirements.txt
# Verify Dockerfiles use correct paths
# Check pytest.ini configuration
```

**Issue**: GHCR push fails
```bash
# Solution: Check repository permissions
# Ensure GitHub token has write access to packages
# Verify repository name is correct
```

**Issue**: Allure report not generated
```bash
# Solution: Ensure allure-results directory exists
# Check that tests ran with --alluredir flag
# Verify simple-elf/allure-report-action version
```

---

## Summary

| Test Type | File(s) | Framework | Count | When It Runs | What It Tests |
|-----------|---------|-----------|-------|--------------|---------------|
| Backend Unit Tests | `backend/tests/unit/*.py` | pytest | 88 | Every commit | Validation, authorization, error handling, CRUD, edge cases |
| Backend Integration Tests | `backend/tests/integration/*.py` | pytest | 8 | Every commit | API endpoint integration with database |
| Selenium E2E Tests | `backend/tests/selenium/*.py` | pytest + Selenium | 2 | Every commit | User workflows with Page Object Model |
| Angular Component Tests | `frontend/src/app/**/*component.spec.ts` | Jasmine/Karma | 78 | Every commit | Component logic, validation, state management |
| JMeter Tests | `database/performance_profile.jmx` | Apache JMeter | 1 | Every commit | API performance under load |
| **Total** | - | - | **177** | - | - |

### Key Improvements (June 2026 Refactor)

**Test Organization**:
- Separated unit tests from integration tests
- Created dedicated Selenium folder with Page Object Model
- Organized tests by feature/module

**Allure Reporting**:
- Added comprehensive Allure decorators to all backend tests
- Implemented proper hierarchy: parent_suite → suite → feature → story
- Added severity levels (CRITICAL, HIGH, MEDIUM)
- Added meaningful test titles and descriptions

**Selenium Enhancements**:
- Implemented Page Object Model pattern
- Created reusable helper methods
- Added automatic screenshot capture on failure
- Added browser console logs attachment
- Added page source and URL attachment on failure
- Split monolithic test into focused workflow tests

**Test Coverage**:
- Backend: 88 new unit tests covering validation, authorization, error handling, CRUD operations, edge cases
- Frontend: 78 new component tests covering all major components
- Total: 177 tests (up from ~15)

**CI/CD Pipeline**:
- Updated test execution paths to match new structure
- Added separate unit and integration test runs
- Added pytest-cov for coverage reporting
- Fixed artifact upload paths
- Improved report packaging

**Code Quality**:
- Removed unused dependencies (html-testRunner)
- Added missing dependencies (pytest-cov, selenium, webdriver-manager)
- Removed duplicate code
- Improved test maintainability

### Dependencies

**Backend** (`backend/requirements.txt`):
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-multipart==0.0.6
passlib==1.7.4
python-jose[cryptography]==3.3.0
bcrypt==4.1.1
python-dotenv==1.0.0
httpx==0.24.0
allure-pytest>=2.13.5
pytest-cov>=4.1.0
selenium>=4.15.0
webdriver-manager>=4.0.0
```

**Frontend** (`frontend/package.json`):
- Angular testing framework (Jasmine/Karma) included by default
- No additional test dependencies required

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
11. **Use Allure Decorators**: Provides comprehensive test reporting
12. **Capture Failure Artifacts**: Screenshots and logs help debug failures
13. **Separate Unit and Integration Tests**: Unit tests should be fast, integration tests can be slower
14. **Test Edge Cases**: Don't just test happy paths
15. **Maintain Test Coverage**: Aim for high coverage but prioritize critical paths

---

## Additional Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [JMeter User Manual](https://jmeter.apache.org/usermanual/index.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Angular Testing Guide](https://angular.io/guide/testing)
- [Pytest Documentation](https://docs.pytest.org/)
- [Allure Test Report](https://allurereport.org/)
- [Page Object Model Pattern](https://www.selenium.dev/documentation/test_practices/encouraged_page_object_models/)

---

## Changelog

### June 29, 2026 - Major Testing Architecture Refactor

**Added**:
- 88 backend unit tests with comprehensive coverage
- 78 Angular component tests
- Page Object Model for Selenium tests
- Selenium helper utilities
- Allure reporting integration
- pytest configuration (pytest.ini)
- Coverage reporting with pytest-cov
- Automatic failure artifacts for Selenium tests

**Modified**:
- Reorganized backend tests into unit/integration/selenium folders
- Updated CI/CD pipeline to match new test structure
- Updated requirements.txt with new dependencies
- Refactored all backend tests with Allure decorators

**Removed**:
- Old monolithic Selenium test file (test_selenium_regression.py)
- Unused dependency (html-testRunner)

**Improved**:
- Test maintainability with Page Object Model
- Test reporting with Allure
- Test coverage from ~15 to 177 tests
- CI/CD pipeline with better artifact handling
- Documentation with comprehensive testing guide
