"""
Pydantic schemas for request/response validation in FastAPI endpoints.

This module defines Pydantic models that validate incoming request data
and structure outgoing response data. Each schema corresponds to a database model
or API endpoint requirement.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# ==========================================
# User Schemas
# ==========================================
class UserBase(BaseModel):
    """Base user schema with common fields."""
    username: str = Field(..., min_length=3, pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$")

class UserCreate(UserBase):
    """Schema for user registration - includes password."""
    password: str = Field(..., min_length=8)

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


# ==========================================
# Income Schemas
# ==========================================
class IncomeBase(BaseModel):
    """Base income schema with common fields."""
    source: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)  # 🌟 Enforces amount > 0 (fixes test_create_income_negative_amount / test_create_income_zero_amount)
    date: datetime
    category: str = Field(..., min_length=1)

class IncomeCreate(IncomeBase):
    """Schema for creating income records."""
    pass

class IncomeUpdate(BaseModel):
    """Schema for updating income records via PUT endpoints."""
    source: Optional[str] = Field(None, min_length=1)
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[datetime] = None
    category: Optional[str] = Field(None, min_length=1)

class Income(IncomeBase):
    """Schema for income response - includes database-generated fields."""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# Expense Schemas
# ==========================================
class ExpenseBase(BaseModel):
    """Base expense schema with common fields."""
    description: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)  # 🌟 Enforces amount > 0 (fixes test_create_expense_negative_amount / test_create_expense_zero_amount)
    date: datetime
    category: str = Field(..., min_length=1)

class ExpenseCreate(ExpenseBase):
    """Schema for creating expense records."""
    pass

class ExpenseUpdate(BaseModel):
    """Schema for updating expense records via PUT endpoints."""
    description: Optional[str] = Field(None, min_length=1)
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[datetime] = None
    category: Optional[str] = Field(None, min_length=1)

class Expense(ExpenseBase):
    """Schema for expense response - includes database-generated fields."""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# Budget Schemas
# ==========================================
class BudgetBase(BaseModel):
    """Base budget schema with common fields."""
    category: str = Field(..., min_length=1)  # 🌟 Enforces category cannot be empty string (fixes test_create_budget_empty_category)
    limit: float = Field(..., gt=0)          # 🌟 Enforces limit > 0 (fixes test_create_budget_negative_limit / test_create_budget_zero_limit)

class BudgetCreate(BudgetBase):
    """Schema for creating budget records."""
    pass

class BudgetUpdate(BaseModel):
    """Schema for updating budget records via PUT endpoints."""
    category: Optional[str] = Field(None, min_length=1)
    limit: Optional[float] = Field(None, gt=0)

class Budget(BudgetBase):
    """Schema for budget response - includes database-generated fields."""
    id: int
    user_id: int
    created_at: datetime
    spent: float = 0.0

    class Config:
        from_attributes = True


# ==========================================
# Dashboard Schemas
# ==========================================
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