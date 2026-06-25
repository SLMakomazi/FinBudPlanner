"""
Budget router for managing budget limits by category.

This module handles CRUD operations for user budget records,
including creating budgets with spending calculations.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Budget, User, Expense
from schemas import BudgetCreate, Budget as BudgetSchema
from auth import get_current_active_user
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/budget", response_model=BudgetSchema)
def create_budget(
    budget: BudgetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new budget for a specific category.
    
    Args:
        budget: Budget data (category, spending limit)
        current_user: The authenticated user
        db: Database session
        
    Returns:
        Budget: The created budget record
        
    Raises:
        HTTPException: If budget for category already exists
    """
    logger.info(f"Creating budget for user '{current_user.username}': {budget.category}, limit {budget.limit}")
    
    # Check if budget for this category already exists
    existing_budget = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.category == budget.category
    ).first()
    
    if existing_budget:
        logger.warning(f"Budget for category '{budget.category}' already exists for user '{current_user.username}'")
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
    
    logger.info(f"Budget created successfully with ID: {db_budget.id}")
    return db_budget

@router.get("/budget", response_model=List[BudgetSchema])
def get_budgets(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all budgets for the current user with spending calculations.
    
    Calculates the amount spent in each category for the current month
    and includes it in the response.
    
    Args:
        current_user: The authenticated user
        db: Database session
        
    Returns:
        List[Budget]: List of budgets with spending amounts
    """
    logger.info(f"Fetching budgets for user '{current_user.username}'")
    budgets = db.query(Budget).filter(Budget.user_id == current_user.id).all()
    
    # Calculate spent amount for each budget
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    for budget in budgets:
        total_spent = db.query(Expense).filter(
            Expense.user_id == current_user.id,
            Expense.category == budget.category,
            Expense.date >= datetime(current_year, current_month, 1)
        ).with_entities(
            db.func.sum(Expense.amount)
        ).scalar() or 0
        
        budget.spent = total_spent
    
    logger.info(f"Found {len(budgets)} budgets for user '{current_user.username}'")
    return budgets

@router.get("/budget/{budget_id}", response_model=BudgetSchema)
def get_budget(
    budget_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific budget by ID with spending calculation.
    
    Args:
        budget_id: The ID of the budget record
        current_user: The authenticated user
        db: Database session
        
    Returns:
        Budget: The requested budget with spending amount
        
    Raises:
        HTTPException: If budget not found or doesn't belong to user
    """
    logger.info(f"Fetching budget {budget_id} for user '{current_user.username}'")
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == current_user.id
    ).first()
    
    if not budget:
        logger.warning(f"Budget {budget_id} not found for user '{current_user.username}'")
        raise HTTPException(status_code=404, detail="Budget not found")
    
    # Calculate spent amount
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    total_spent = db.query(Expense).filter(
        Expense.user_id == current_user.id,
        Expense.category == budget.category,
        Expense.date >= datetime(current_year, current_month, 1)
    ).with_entities(
        db.func.sum(Expense.amount)
    ).scalar() or 0
    
    budget.spent = total_spent
    
    return budget

@router.delete("/budget/{budget_id}")
def delete_budget(
    budget_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific budget record.
    
    Args:
        budget_id: The ID of the budget record to delete
        current_user: The authenticated user
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If budget not found or doesn't belong to user
    """
    logger.info(f"Deleting budget {budget_id} for user '{current_user.username}'")
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == current_user.id
    ).first()
    
    if not budget:
        logger.warning(f"Budget {budget_id} not found for user '{current_user.username}'")
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db.delete(budget)
    db.commit()
    logger.info(f"Budget {budget_id} deleted successfully")
    return {"message": "Budget deleted successfully"}
