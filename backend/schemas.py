"""
Pydantic schemas for request/response validation in FastAPI endpoints.

This module defines Pydantic models that validate incoming request data
and structure outgoing response data. Each schema corresponds to a database model
or API endpoint requirement.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    """Base user schema with common fields."""
    username: str

class UserCreate(UserBase):
    """Schema for user registration - includes password."""
    password: str

class User(UserBase):
    """Schema for user response - includes database-generated fields."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Allows creating from ORM models

class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for JWT token payload data."""
    username: Optional[str] = None

# Income Schemas
class IncomeBase(BaseModel):
    """Base income schema with common fields."""
    source: str
    amount: float
    date: datetime
    category: str

class IncomeCreate(IncomeBase):
    """Schema for creating income records."""
    pass

class Income(IncomeBase):
    """Schema for income response - includes database-generated fields."""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Expense Schemas
class ExpenseBase(BaseModel):
    """Base expense schema with common fields."""
    description: str
    amount: float
    date: datetime
    category: str

class ExpenseCreate(ExpenseBase):
    """Schema for creating expense records."""
    pass

class Expense(ExpenseBase):
    """Schema for expense response - includes database-generated fields."""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Budget Schemas
class BudgetBase(BaseModel):
    """Base budget schema with common fields."""
    category: str
    limit: float

class BudgetCreate(BudgetBase):
    """Schema for creating budget records."""
    pass

class Budget(BudgetBase):
    """Schema for budget response - includes database-generated fields."""
    id: int
    user_id: int
    created_at: datetime
    spent: float = 0.0

    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardSummary(BaseModel):
    """Schema for dashboard financial summary."""
    total_income: float
    total_expenses: float
    net_balance: float
    savings_rate: float

class CategorySpending(BaseModel):
    """Schema for expense breakdown by category."""
    category: str
    amount: float
