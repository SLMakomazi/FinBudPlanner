import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

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
  http;
  apiUrl = 'http://localhost:8000/api';

  constructor(router: Router, http: HttpClient) {
    console.log('[ExpenseComponent] Constructor called');
    this.router = router;
    this.http = http;
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
    console.log('[ExpenseComponent] Loading expense data from backend');
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.get(`${this.apiUrl}/expense`, { headers }).subscribe({
      next: (data: any) => {
        this.expenseList = data;
        console.log('[ExpenseComponent] Loaded', this.expenseList.length, 'expense records from backend');
      },
      error: (error) => {
        console.error('[ExpenseComponent] Error loading expense data:', error);
        this.errorMessage = 'Failed to load expense data. Please check your connection.';
      }
    });
  }

  saveExpenseData() {
    console.log('[ExpenseComponent] saveExpenseData - using backend API, no localStorage save needed');
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
      description: this.newExpense.description,
      amount: Number(this.newExpense.amount),
      date: new Date(this.newExpense.date).toISOString(),
      category: this.newExpense.category
    };

    console.log('[ExpenseComponent] Adding expense record via backend:', expense);
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.post(`${this.apiUrl}/expense`, expense, { headers }).subscribe({
      next: (data: any) => {
        console.log('[ExpenseComponent] Expense added successfully via backend:', data);
        this.expenseList.push(data);
        
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
      },
      error: (error) => {
        console.error('[ExpenseComponent] Error adding expense:', error);
        this.errorMessage = 'Failed to add expense. Please try again.';
      }
    });
  }

  deleteExpense(id) {
    console.log('[ExpenseComponent] deleteExpense called for id:', id);
    if (confirm('Are you sure you want to delete this expense record?')) {
      const token = localStorage.getItem('token');
      const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
      
      this.http.delete(`${this.apiUrl}/expense/${id}`, { headers }).subscribe({
        next: () => {
          console.log('[ExpenseComponent] Expense deleted successfully via backend');
          this.expenseList = this.expenseList.filter(expense => expense.id !== id);
        },
        error: (error) => {
          console.error('[ExpenseComponent] Error deleting expense:', error);
          alert('Failed to delete expense. Please try again.');
        }
      });
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
