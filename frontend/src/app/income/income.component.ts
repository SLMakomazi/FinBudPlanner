import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-income',
  templateUrl: './income.component.html',
  styleUrls: ['./income.component.css']
})
export class IncomeComponent {
  showAddForm = false;
  errorMessage = '';
  incomeList = [];
  newIncome = {
    source: '',
    amount: 0,
    date: '',
    category: ''
  };

  router;

  constructor(router: Router) {
    console.log('[IncomeComponent] Constructor called');
    this.router = router;
    this.loadIncomeData();
    this.setDefaultDate();
  }

  ngOnInit() {
    console.log('[IncomeComponent] ngOnInit called');
  }

  setDefaultDate() {
    const today = new Date();
    this.newIncome.date = today.toISOString().split('T')[0];
    console.log('[IncomeComponent] Default date set:', this.newIncome.date);
  }

  loadIncomeData() {
    console.log('[IncomeComponent] Loading income data');
    const storedData = localStorage.getItem('incomeData');
    if (storedData) {
      this.incomeList = JSON.parse(storedData);
      console.log('[IncomeComponent] Loaded', this.incomeList.length, 'income records');
    } else {
      console.log('[IncomeComponent] No income data found');
    }
  }

  saveIncomeData() {
    console.log('[IncomeComponent] Saving income data', this.incomeList.length, 'records');
    localStorage.setItem('incomeData', JSON.stringify(this.incomeList));
  }

  get totalMonthlyIncome() {
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    
    return this.incomeList
      .filter(income => {
        const incomeDate = new Date(income.date);
        return incomeDate.getMonth() === currentMonth && 
               incomeDate.getFullYear() === currentYear;
      })
      .reduce((total, income) => total + income.amount, 0);
  }

  get currentMonth() {
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December'];
    return months[new Date().getMonth()];
  }

  onAddIncome() {
    console.log('[IncomeComponent] onAddIncome called', this.newIncome);
    
    if (!this.newIncome.source || !this.newIncome.amount || !this.newIncome.date || !this.newIncome.category) {
      this.errorMessage = 'Please fill in all fields';
      console.log('[IncomeComponent] Validation failed: missing fields');
      return;
    }

    if (this.newIncome.amount <= 0) {
      this.errorMessage = 'Amount must be greater than 0';
      console.log('[IncomeComponent] Validation failed: amount <= 0');
      return;
    }

    const income = {
      id: Date.now(),
      source: this.newIncome.source,
      amount: Number(this.newIncome.amount),
      date: this.newIncome.date,
      category: this.newIncome.category
    };

    console.log('[IncomeComponent] Adding income record:', income);
    this.incomeList.push(income);
    this.saveIncomeData();
    
    // Reset form
    this.newIncome = {
      source: '',
      amount: 0,
      date: '',
      category: ''
    };
    this.setDefaultDate();
    this.showAddForm = false;
    this.errorMessage = '';
    console.log('[IncomeComponent] Income added successfully');
  }

  deleteIncome(id) {
    console.log('[IncomeComponent] deleteIncome called for id:', id);
    if (confirm('Are you sure you want to delete this income record?')) {
      this.incomeList = this.incomeList.filter(income => income.id !== id);
      this.saveIncomeData();
      console.log('[IncomeComponent] Income deleted successfully');
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
}
