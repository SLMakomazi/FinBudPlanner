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
    this.router = router;
    this.loadIncomeData();
    this.setDefaultDate();
  }

  setDefaultDate() {
    const today = new Date();
    this.newIncome.date = today.toISOString().split('T')[0];
  }

  loadIncomeData() {
    const storedData = localStorage.getItem('incomeData');
    if (storedData) {
      this.incomeList = JSON.parse(storedData);
    }
  }

  saveIncomeData() {
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
    if (!this.newIncome.source || !this.newIncome.amount || !this.newIncome.date || !this.newIncome.category) {
      this.errorMessage = 'Please fill in all fields';
      return;
    }

    if (this.newIncome.amount <= 0) {
      this.errorMessage = 'Amount must be greater than 0';
      return;
    }

    const income = {
      id: Date.now(),
      source: this.newIncome.source,
      amount: Number(this.newIncome.amount),
      date: this.newIncome.date,
      category: this.newIncome.category
    };

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
  }

  deleteIncome(id) {
    if (confirm('Are you sure you want to delete this income record?')) {
      this.incomeList = this.incomeList.filter(income => income.id !== id);
      this.saveIncomeData();
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
