"""
Expense router for managing expense records.

This module handles CRUD operations for user expense records,
including creating, reading, and deleting expense entries.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Expense, User
from schemas import ExpenseCreate, Expense as ExpenseSchema, ExpenseUpdate
from auth import get_current_active_user
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/expense", response_model=ExpenseSchema)
def create_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new expense record for the current user.
    
    Args:
        expense: Expense data (description, amount, date, category)
        current_user: The authenticated user
        db: Database session
        
    Returns:
        Expense: The created expense record
    """
    logger.info(f"Creating expense record for user '{current_user.username}': {expense.description}, {expense.amount}")
    
    db_expense = Expense(
        user_id=current_user.id,
        description=expense.description,
        amount=expense.amount,
        date=expense.date,
        category=expense.category
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    logger.info(f"Expense record created successfully with ID: {db_expense.id}")
    return db_expense

@router.get("/expense", response_model=List[ExpenseSchema])
def get_expenses(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all expense records for the current user.
    
    Args:
        current_user: The authenticated user
        db: Database session
        
    Returns:
        List[Expense]: List of all expense records for the user
    """
    logger.info(f"Fetching expense records for user '{current_user.username}'")
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    logger.info(f"Found {len(expenses)} expense records for user '{current_user.username}'")
    return expenses

@router.get("/expense/{expense_id}", response_model=ExpenseSchema)
def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific expense record by ID.
    
    Args:
        expense_id: The ID of the expense record
        current_user: The authenticated user
        db: Database session
        
    Returns:
        Expense: The requested expense record
        
    Raises:
        HTTPException: If expense not found or doesn't belong to user
    """
    logger.info(f"Fetching expense record {expense_id} for user '{current_user.username}'")
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    if not expense:
        logger.warning(f"Expense record {expense_id} not found for user '{current_user.username}'")
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.delete("/expense/{expense_id}")
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific expense record.
    
    Args:
        expense_id: The ID of the expense record to delete
        current_user: The authenticated user
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If expense not found or doesn't belong to user
    """
    logger.info(f"Deleting expense record {expense_id} for user '{current_user.username}'")
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    if not expense:
        logger.warning(f"Expense record {expense_id} not found for user '{current_user.username}'")
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    logger.info(f"Expense record {expense_id} deleted successfully")
    return {"message": "Expense deleted successfully"}

# =========================
# UPDATE EXPENSE
# =========================
@router.put("/expense/{expense_id}", response_model=ExpenseSchema)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a specific expense record."""
    logger.info(f"Updating expense record {expense_id} for user '{current_user.username}'")
    
    db_expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not db_expense:
        logger.warning(f"Expense record {expense_id} not found for user '{current_user.username}'")
        raise HTTPException(status_code=404, detail="Expense not found")
        
    update_data = expense_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)
        
    db.commit()
    db.refresh(db_expense)
    
    logger.info(f"Expense record {expense_id} updated successfully")
    return db_expense
