import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_index, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db  # <-- Adjust these imports based on your actual file paths

# 1. Setup an isolated, in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Needed to share the in-memory DB across connections
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Creates tables before each test and drops them immediately after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Provides a clean database session if you need to manually seed data in tests."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_client():
    """Overrides the FastAPI app's database dependency to use the test database."""
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
            
    # Force FastAPI to swap the real DB session for our isolated test DB session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    # Clean up overrides after the test finishes
    app.dependency_overrides.clear()


@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "password": "TestPass123!"
    }


@pytest.fixture
def auth_headers(test_client, test_user):
    # This will now succeed cleanly every time because setup_database() wipes the DB before the test runs
    test_client.post("/api/register", json=test_user)

    response = test_client.post(
        "/api/token",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }