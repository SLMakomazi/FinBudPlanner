"""
Database configuration and session management for FinBudPlanner backend.

This module sets up the SQLAlchemy database engine, session factory,
and provides a dependency for getting database sessions in FastAPI endpoints.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database path in the database folder
# Constructs path to ../database/finbud.db relative to this file
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'finbud.db')

# SQLAlchemy database URL for SQLite
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create the database engine
# check_same_thread=False is required for SQLite to allow multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory for database sessions
# autocommit=False and autoflush=False for manual transaction control
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
# All database models will inherit from this Base class
Base = declarative_base()

def get_db():
    """
    Dependency function for FastAPI to get database sessions.
    
    This function is used as a dependency in FastAPI endpoints to provide
    a database session. It ensures proper session cleanup after each request.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
