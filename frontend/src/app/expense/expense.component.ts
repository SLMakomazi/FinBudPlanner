import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-expense',
  templateUrl: './expense.component.html',
  styleUrls: ['./expense.component.css']
})
export class ExpenseComponent {
  showAddForm = false;
  errorMessage = '';
  expenseList = [];
  newExpense = {
    description: '',
    amount: 0,
    date: '',
    category: ''
  };

  router;

  constructor(router: Router) {
    this.router = router;
    this.loadExpenseData();
    this.setDefaultDate();
  }

  setDefaultDate() {
    const today = new Date();
    this.newExpense.date = today.toISOString().split('T')[0];
  }

  loadExpenseData() {
    const storedData = localStorage.getItem('expenseData');
    if (storedData) {
      this.expenseList = JSON.parse(storedData);
    }
  }

  saveExpenseData() {
    localStorage.setItem('expenseData', JSON.stringify(this.expenseList));
  }

  get totalMonthlyExpenses() {
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    
    return this.expenseList
      .filter(expense => {
        const expenseDate = new Date(expense.date);
        return expenseDate.getMonth() === currentMonth && 
               expenseDate.getFullYear() === currentYear;
      })
      .reduce((total, expense) => total + expense.amount, 0);
  }

  get currentMonth() {
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December'];
    return months[new Date().getMonth()];
  }

  onAddExpense() {
    if (!this.newExpense.description || !this.newExpense.amount || !this.newExpense.date || !this.newExpense.category) {
      this.errorMessage = 'Please fill in all fields';
      return;
    }

    if (this.newExpense.amount <= 0) {
      this.errorMessage = 'Amount must be greater than 0';
      return;
    }

    const expense = {
      id: Date.now(),
      description: this.newExpense.description,
      amount: Number(this.newExpense.amount),
      date: this.newExpense.date,
      category: this.newExpense.category
    };

    this.expenseList.push(expense);
    this.saveExpenseData();
    
    // Reset form
    this.newExpense = {
      description: '',
      amount: 0,
      date: '',
      category: ''
    };
    this.setDefaultDate();
    this.showAddForm = false;
    this.errorMessage = '';
  }

  deleteExpense(id) {
    if (confirm('Are you sure you want to delete this expense record?')) {
      this.expenseList = this.expenseList.filter(expense => expense.id !== id);
      this.saveExpenseData();
    }
  }

  formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  }

  formatCategory(category) {
    const categoryMap = {
      'food': 'Food & Dining',
      'transportation': 'Transportation',
      'utilities': 'Utilities',
      'entertainment': 'Entertainment',
      'shopping': 'Shopping',
      'healthcare': 'Healthcare',
      'education': 'Education',
      'other': 'Other'
    };
    return categoryMap[category] || category;
  }
}
