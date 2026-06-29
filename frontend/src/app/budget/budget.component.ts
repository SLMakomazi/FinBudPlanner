import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-budget',
  templateUrl: './budget.component.html',
  styleUrls: ['./budget.component.css']
})
export class BudgetComponent {
  showAddForm = false;
  errorMessage = '';
  budgetList = [];
  newBudget = {
    category: '',
    limit: 0
  };

  router;
  http;
  apiUrl = 'http://localhost:8000/api';

  get totalBudget(): number {
    return this.budgetList.reduce((sum, b) => sum + (Number(b.limit) || 0), 0);
  }

  get totalSpent(): number {
    return this.budgetList.reduce((sum, b) => sum + (Number(b.spent) || 0), 0);
  }

  get remainingBudget(): number {
    return this.totalBudget - this.totalSpent;
  }

  constructor(router: Router, http: HttpClient) {
    console.log('[BudgetComponent] Constructor called');
    this.router = router;
    this.http = http;
    this.loadBudgetData();
  }

  ngOnInit() {
    console.log('[BudgetComponent] ngOnInit called');
  }

  loadBudgetData() {
    console.log('[BudgetComponent] Loading budget data from backend');
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.get(`${this.apiUrl}/budget`, { headers }).subscribe({
      next: (data: any) => {
        this.budgetList = data;
        console.log('[BudgetComponent] Loaded', this.budgetList.length, 'budget records from backend');
      },
      error: (error) => {
        console.error('[BudgetComponent] Error loading budget data:', error);
        this.errorMessage = 'Failed to load budget data. Please check your connection.';
      }
    });
  }

  saveBudgetData() {
    console.log('[BudgetComponent] saveBudgetData - using backend API, no localStorage save needed');
  }

  updateBudgetSpending() {
    console.log('[BudgetComponent] Budget spending is calculated by backend, no local calculation needed');
  }

  onAddBudget() {
    console.log('[BudgetComponent] onAddBudget called', this.newBudget);
    
    if (!this.newBudget.category || !this.newBudget.limit) {
      this.errorMessage = 'Please fill in all fields';
      console.log('[BudgetComponent] Validation failed: missing fields');
      return;
    }

    if (this.newBudget.limit <= 0) {
      this.errorMessage = 'Limit must be greater than 0';
      console.log('[BudgetComponent] Validation failed: limit <= 0');
      return;
    }

    const budget = {
      category: this.newBudget.category,
      limit: Number(this.newBudget.limit)
    };

    console.log('[BudgetComponent] Adding budget record via backend:', budget);
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.post(`${this.apiUrl}/budget`, budget, { headers }).subscribe({
      next: (data: any) => {
        console.log('[BudgetComponent] Budget added successfully via backend:', data);
        this.budgetList.push(data);
        
        // Reset form
        this.newBudget = {
          category: '',
          limit: 0
        };
        this.showAddForm = false;
        this.errorMessage = '';
      },
      error: (error) => {
        console.error('[BudgetComponent] Error adding budget:', error);
        if (error.status === 400) {
          this.errorMessage = 'Budget for this category already exists. Delete it first to set a new one.';
        } else {
          this.errorMessage = 'Failed to add budget. Please try again.';
        }
      }
    });
  }

  deleteBudget(id) {
    console.log('[BudgetComponent] deleteBudget called for id:', id);
    if (confirm('Are you sure you want to delete this budget?')) {
      const token = localStorage.getItem('token');
      const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
      
      this.http.delete(`${this.apiUrl}/budget/${id}`, { headers }).subscribe({
        next: () => {
          console.log('[BudgetComponent] Budget deleted successfully via backend');
          this.budgetList = this.budgetList.filter(budget => budget.id !== id);
        },
        error: (error) => {
          console.error('[BudgetComponent] Error deleting budget:', error);
          alert('Failed to delete budget. Please try again.');
        }
      });
    }
  }

  getProgressPercentage(spent, limit) {
    if (limit === 0) return 0;
    return (spent / limit) * 100;
  }

  getProgressClass(spent, limit) {
    const percentage = this.getProgressPercentage(spent, limit);
    if (percentage >= 100) return 'danger';
    if (percentage >= 80) return 'warning';
    return 'success';
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
