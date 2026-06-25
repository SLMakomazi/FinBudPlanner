"""
Income router for managing income records.

This module handles CRUD operations for user income records,
including creating, reading, and deleting income entries.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Income, User
from schemas import IncomeCreate, Income as IncomeSchema
from auth import get_current_active_user
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/income", response_model=IncomeSchema)
def create_income(
    income: IncomeCreate, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new income record for the current user.
    
    Args:
        income: Income data (source, amount, date, category)
        current_user: The authenticated user
        db: Database session
        
    Returns:
        Income: The created income record
    """
    logger.info(f"Creating income record for user '{current_user.username}': {income.source}, {income.amount}")
    
    db_income = Income(
        user_id=current_user.id,
        source=income.source,
        amount=income.amount,
        date=income.date,
        category=income.category
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    
    logger.info(f"Income record created successfully with ID: {db_income.id}")
    return db_income

@router.get("/income", response_model=List[IncomeSchema])
def get_incomes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all income records for the current user.
    
    Args:
        current_user: The authenticated user
        db: Database session
        
    Returns:
        List[Income]: List of all income records for the user
    """
    logger.info(f"Fetching income records for user '{current_user.username}'")
    incomes = db.query(Income).filter(Income.user_id == current_user.id).all()
    logger.info(f"Found {len(incomes)} income records for user '{current_user.username}'")
    return incomes

@router.get("/income/{income_id}", response_model=IncomeSchema)
def get_income(
    income_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific income record by ID.
    
    Args:
        income_id: The ID of the income record
        current_user: The authenticated user
        db: Database session
        
    Returns:
        Income: The requested income record
        
    Raises:
        HTTPException: If income not found or doesn't belong to user
    """
    logger.info(f"Fetching income record {income_id} for user '{current_user.username}'")
    income = db.query(Income).filter(
        Income.id == income_id,
        Income.user_id == current_user.id
    ).first()
    if not income:
        logger.warning(f"Income record {income_id} not found for user '{current_user.username}'")
        raise HTTPException(status_code=404, detail="Income not found")
    return income

@router.delete("/income/{income_id}")
def delete_income(
    income_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific income record.
    
    Args:
        income_id: The ID of the income record to delete
        current_user: The authenticated user
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If income not found or doesn't belong to user
    """
    logger.info(f"Deleting income record {income_id} for user '{current_user.username}'")
    income = db.query(Income).filter(
        Income.id == income_id,
        Income.user_id == current_user.id
    ).first()
    if not income:
        logger.warning(f"Income record {income_id} not found for user '{current_user.username}'")
        raise HTTPException(status_code=404, detail="Income not found")
    db.delete(income)
    db.commit()
    logger.info(f"Income record {income_id} deleted successfully")
    return {"message": "Income deleted successfully"}
