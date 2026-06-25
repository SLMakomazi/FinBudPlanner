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
    console.log('[ExpenseComponent] Constructor called');
    this.router = router;
    this.loadExpenseData();
    this.setDefaultDate();
  }

  ngOnInit() {
    console.log('[ExpenseComponent] ngOnInit called');
  }

  setDefaultDate() {
    const today = new Date();
    this.newExpense.date = today.toISOString().split('T')[0];
    console.log('[ExpenseComponent] Default date set:', this.newExpense.date);
  }

  loadExpenseData() {
    console.log('[ExpenseComponent] Loading expense data');
    const storedData = localStorage.getItem('expenseData');
    if (storedData) {
      this.expenseList = JSON.parse(storedData);
      console.log('[ExpenseComponent] Loaded', this.expenseList.length, 'expense records');
    } else {
      console.log('[ExpenseComponent] No expense data found');
    }
  }

  saveExpenseData() {
    console.log('[ExpenseComponent] Saving expense data', this.expenseList.length, 'records');
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
    console.log('[ExpenseComponent] onAddExpense called', this.newExpense);
    
    if (!this.newExpense.description || !this.newExpense.amount || !this.newExpense.date || !this.newExpense.category) {
      this.errorMessage = 'Please fill in all fields';
      console.log('[ExpenseComponent] Validation failed: missing fields');
      return;
    }

    if (this.newExpense.amount <= 0) {
      this.errorMessage = 'Amount must be greater than 0';
      console.log('[ExpenseComponent] Validation failed: amount <= 0');
      return;
    }

    const expense = {
      id: Date.now(),
      description: this.newExpense.description,
      amount: Number(this.newExpense.amount),
      date: this.newExpense.date,
      category: this.newExpense.category
    };

    console.log('[ExpenseComponent] Adding expense record:', expense);
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
    console.log('[ExpenseComponent] Expense added successfully');
  }

  deleteExpense(id) {
    console.log('[ExpenseComponent] deleteExpense called for id:', id);
    if (confirm('Are you sure you want to delete this expense record?')) {
      this.expenseList = this.expenseList.filter(expense => expense.id !== id);
      this.saveExpenseData();
      console.log('[ExpenseComponent] Expense deleted successfully');
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
