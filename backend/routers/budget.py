"""
Budget router for managing budget limits by category.

Handles CRUD operations for user budgets and calculates monthly spending.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime 
from database import get_db
from models import Budget, User, Expense
from schemas import BudgetCreate, Budget as BudgetSchema, BudgetUpdate
from auth import get_current_active_user

import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


# =========================
# CREATE BUDGET
# =========================
@router.post("/budget", response_model=BudgetSchema)
def create_budget(
    budget: BudgetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Creating budget for user '{current_user.username}'")

    existing_budget = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.category == budget.category
    ).first()

    if existing_budget:
        raise HTTPException(
            status_code=400,
            detail="Budget for this category already exists"
        )

    db_budget = Budget(
        user_id=current_user.id,
        category=budget.category,
        limit=budget.limit
    )

    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)

    return db_budget


# =========================
# GET ALL BUDGETS
# =========================
@router.get("/budget", response_model=List[BudgetSchema])
def get_budgets(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching budgets for user '{current_user.username}'")

    budgets = db.query(Budget).filter(
        Budget.user_id == current_user.id
    ).all()

    # Proper month start calculation (IMPORTANT FIX)
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)

    for budget in budgets:
        total_spent = db.query(
            func.coalesce(func.sum(Expense.amount), 0)
        ).filter(
            Expense.user_id == current_user.id,
            Expense.category == budget.category,
            Expense.date >= month_start
        ).scalar()

        budget.spent = float(total_spent or 0)

    return budgets


# =========================
# GET SINGLE BUDGET
# =========================
@router.get("/budget/{budget_id}", response_model=BudgetSchema)
def get_budget(
    budget_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == current_user.id
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)

    total_spent = db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.user_id == current_user.id,
        Expense.category == budget.category,
        Expense.date >= month_start
    ).scalar()

    budget.spent = float(total_spent or 0)

    return budget


# =========================
# DELETE BUDGET
# =========================
@router.delete("/budget/{budget_id}")
def delete_budget(
    budget_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == current_user.id
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(budget)
    db.commit()

    return {"message": "Budget deleted successfully"}



# =========================
# UPDATE BUDGET
# =========================
@router.put("/budget/{budget_id}", response_model=BudgetSchema)
def update_budget(
    budget_id: int,
    budget_update: BudgetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Updating budget ID {budget_id} for user '{current_user.username}'")

    # 1. Look up the budget and ensure ownership
    db_budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == current_user.id
    ).first()

    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    # 2. Update provided fields dynamically
    update_data = budget_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_budget, key, value)

    db.commit()
    db.refresh(db_budget)

    # 3. Calculate current month's spending so response matches schema requirements
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)

    total_spent = db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.user_id == current_user.id,
        Expense.category == db_budget.category,
        Expense.date >= month_start
    ).scalar()

    db_budget.spent = float(total_spent or 0)

    return db_budget