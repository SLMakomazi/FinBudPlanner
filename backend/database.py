"""
Database configuration and session management for FinBudPlanner backend.
Docker-safe + local-safe SQLite setup.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ==============================
# 1. Build safe database path
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")

# Ensure directory exists (CRITICAL for Docker)
os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "finbud.db")

# ==============================
# 2. SQLite URL
# ==============================

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# ==============================
# 3. Engine
# ==============================

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# ==============================
# 4. Session
# ==============================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ==============================
# 5. Base ORM
# ==============================

Base = declarative_base()

# ==============================
# 6. Dependency
# ==============================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()