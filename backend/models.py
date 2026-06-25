"""
SQLAlchemy ORM models for FinBudPlanner database.

This module defines all database tables as Python classes using SQLAlchemy ORM.
Each class represents a table in the SQLite database with relationships between them.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    """
    User model representing application users.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        username: Unique username for login (indexed for fast lookups)
        hashed_password: Bcrypt hashed password for security
        created_at: Timestamp when user account was created
        incomes: Relationship to user's income records
        expenses: Relationship to user's expense records
        budgets: Relationship to user's budget records
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships to child records
    incomes = relationship("Income", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("Budget", back_populates="user")

class Income(Base):
    """
    Income model representing user's income records.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        user_id: Foreign key to users table (who owns this income)
        source: Source of income (e.g., "Salary", "Freelance")
        amount: Monetary amount of the income
        date: Date when income was received
        category: Category for income (e.g., "salary", "investment")
        created_at: Timestamp when record was created
        user: Relationship to the user who owns this income
    """
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="incomes")

class Expense(Base):
    """
    Expense model representing user's expense records.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        user_id: Foreign key to users table (who owns this expense)
        description: Description of the expense (e.g., "Grocery shopping")
        amount: Monetary amount of the expense
        date: Date when expense occurred
        category: Category for expense (e.g., "food", "transportation")
        created_at: Timestamp when record was created
        user: Relationship to the user who owns this expense
    """
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="expenses")

class Budget(Base):
    """
    Budget model representing user's budget limits by category.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        user_id: Foreign key to users table (who owns this budget)
        category: Category for budget (e.g., "food", "entertainment")
        limit: Maximum spending limit for this category
        created_at: Timestamp when budget was created
        user: Relationship to the user who owns this budget
    """
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    limit = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="budgets")
