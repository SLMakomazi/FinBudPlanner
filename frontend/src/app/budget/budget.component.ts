import { Component } from '@angular/core';
import { Router } from '@angular/router';

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

  constructor(router: Router) {
    console.log('[BudgetComponent] Constructor called');
    this.router = router;
    this.loadBudgetData();
    this.updateBudgetSpending();
  }

  ngOnInit() {
    console.log('[BudgetComponent] ngOnInit called');
  }

  loadBudgetData() {
    console.log('[BudgetComponent] Loading budget data');
    const storedData = localStorage.getItem('budgetData');
    if (storedData) {
      this.budgetList = JSON.parse(storedData);
      console.log('[BudgetComponent] Loaded', this.budgetList.length, 'budget records');
    } else {
      console.log('[BudgetComponent] No budget data found');
    }
  }

  saveBudgetData() {
    console.log('[BudgetComponent] Saving budget data', this.budgetList.length, 'records');
    localStorage.setItem('budgetData', JSON.stringify(this.budgetList));
  }

  updateBudgetSpending() {
    console.log('[BudgetComponent] Updating budget spending');
    // Load expense data to calculate spending
    const expenseData = localStorage.getItem('expenseData');
    const expenses = expenseData ? JSON.parse(expenseData) : [];
    console.log('[BudgetComponent] Loaded', expenses.length, 'expense records for budget calculation');
    
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    
    this.budgetList = this.budgetList.map(budget => {
      const categoryExpenses = expenses
        .filter(expense => {
          const expenseDate = new Date(expense.date);
          return expense.category === budget.category &&
                 expenseDate.getMonth() === currentMonth &&
                 expenseDate.getFullYear() === currentYear;
        })
        .reduce((total, expense) => total + expense.amount, 0);
      
      return {
        ...budget,
        spent: categoryExpenses
      };
    });
    
    this.saveBudgetData();
    console.log('[BudgetComponent] Budget spending updated');
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

    // Check if budget for this category already exists
    const existingBudget = this.budgetList.find(b => b.category === this.newBudget.category);
    if (existingBudget) {
      this.errorMessage = 'Budget for this category already exists. Delete it first to set a new one.';
      console.log('[BudgetComponent] Validation failed: budget already exists for category');
      return;
    }

    const budget = {
      id: Date.now(),
      category: this.newBudget.category,
      limit: Number(this.newBudget.limit),
      spent: 0
    };

    console.log('[BudgetComponent] Adding budget record:', budget);
    this.budgetList.push(budget);
    this.saveBudgetData();
    
    // Reset form
    this.newBudget = {
      category: '',
      limit: 0
    };
    this.showAddForm = false;
    this.errorMessage = '';
    console.log('[BudgetComponent] Budget added successfully');
  }

  deleteBudget(id) {
    console.log('[BudgetComponent] deleteBudget called for id:', id);
    if (confirm('Are you sure you want to delete this budget?')) {
      this.budgetList = this.budgetList.filter(budget => budget.id !== id);
      this.saveBudgetData();
      console.log('[BudgetComponent] Budget deleted successfully');
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
