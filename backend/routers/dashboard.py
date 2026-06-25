"""
Dashboard router for financial summaries and analytics.

This module provides endpoints for generating financial summaries,
expense breakdowns by category, and recent transaction history
for the dashboard view.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Income, Expense, Budget, User
from schemas import DashboardSummary, CategorySpending
from auth import get_current_active_user
from datetime import datetime
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/dashboard/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get financial summary for the current month.
    
    Calculates total income, total expenses, net balance, and savings rate
    for the current month.
    
    Args:
        current_user: The authenticated user
        db: Database session
        
    Returns:
        DashboardSummary: Financial summary with income, expenses, balance, and savings rate
    """
    logger.info(f"Fetching dashboard summary for user '{current_user.username}'")
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    # Calculate total income for current month
    total_income = db.query(func.sum(Income.amount)).filter(
        Income.user_id == current_user.id,
        Income.date >= datetime(current_year, current_month, 1)
    ).scalar() or 0
    
    # Calculate total expenses for current month
    total_expenses = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        Expense.date >= datetime(current_year, current_month, 1)
    ).scalar() or 0
    
    # Calculate net balance
    net_balance = total_income - total_expenses
    
    # Calculate savings rate (percentage of income saved)
    savings_rate = 0
    if total_income > 0:
        savings_rate = ((total_income - total_expenses) / total_income) * 100
    
    logger.info(f"Dashboard summary for user '{current_user.username}': income={total_income}, expenses={total_expenses}, balance={net_balance}")
    return DashboardSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        savings_rate=savings_rate
    )

@router.get("/dashboard/expenses-by-category", response_model=List[CategorySpending])
def get_expenses_by_category(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get expense breakdown by category for the current month.
    
    Groups expenses by category and calculates total spending per category.
    Useful for pie charts and spending analysis.
    
    Args:
        current_user: The authenticated user
        db: Database session
        
    Returns:
        List[CategorySpending]: List of categories with total spending amounts
    """
    logger.info(f"Fetching expenses by category for user '{current_user.username}'")
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    # Get expenses grouped by category for current month
    category_spending = db.query(
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).filter(
        Expense.user_id == current_user.id,
        Expense.date >= datetime(current_year, current_month, 1)
    ).group_by(Expense.category).all()
    
    result = [
        CategorySpending(category=category, total=total)
        for category, total in category_spending
    ]
    logger.info(f"Found {len(result)} expense categories for user '{current_user.username}'")
    return result

@router.get("/dashboard/recent-transactions")
def get_recent_transactions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = 5
):
    """
    Get recent transactions (both income and expenses).
    
    Combines recent income and expense records, sorts by date,
    and returns the most recent transactions.
    
    Args:
        current_user: The authenticated user
        db: Database session
        limit: Maximum number of transactions to return (default: 5)
        
    Returns:
        List[dict]: List of recent transactions with type, description, amount, date, category
    """
    logger.info(f"Fetching recent transactions for user '{current_user.username}' (limit: {limit})")
    # Get recent income transactions
    recent_income = db.query(Income).filter(
        Income.user_id == current_user.id
    ).order_by(Income.date.desc()).limit(limit).all()
    
    # Get recent expense transactions
    recent_expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id
    ).order_by(Expense.date.desc()).limit(limit).all()
    
    # Combine and format transactions
    transactions = []
    
    for income in recent_income:
        transactions.append({
            "id": income.id,
            "type": "income",
            "description": income.source,
            "amount": income.amount,
            "date": income.date,
            "category": income.category
        })
    
    for expense in recent_expenses:
        transactions.append({
            "id": expense.id,
            "type": "expense",
            "description": expense.description,
            "amount": expense.amount,
            "date": expense.date,
            "category": expense.category
        })
    
    # Sort by date (most recent first) and limit results
    transactions.sort(key=lambda x: x['date'], reverse=True)
    
    result = transactions[:limit]
    logger.info(f"Returning {len(result)} recent transactions for user '{current_user.username}'")
    return result
