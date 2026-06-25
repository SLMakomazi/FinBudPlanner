import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

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
  http;
  apiUrl = ['http://127.0.0.1:8000/api','http://localhost:8000/api'];

  constructor(router: Router, http: HttpClient) {
    console.log('[IncomeComponent] Constructor called');
    this.router = router;
    this.http = http;
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
    console.log('[IncomeComponent] Loading income data from backend');
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.get(`${this.apiUrl[0]}/income`, { headers }).subscribe({
      next: (data: any) => {
        this.incomeList = data;
        console.log('[IncomeComponent] Loaded', this.incomeList.length, 'income records from backend');
      },
      error: (error) => {
        console.error('[IncomeComponent] Error loading income data:', error);
        this.errorMessage = 'Failed to load income data. Please check your connection.';
      }
    });
  }

  saveIncomeData() {
    console.log('[IncomeComponent] saveIncomeData - using backend API, no localStorage save needed');
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
      source: this.newIncome.source,
      amount: Number(this.newIncome.amount),
      date: new Date(this.newIncome.date).toISOString(),
      category: this.newIncome.category
    };

    console.log('[IncomeComponent] Adding income record via backend:', income);
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.post(`${this.apiUrl}/income`, income, { headers }).subscribe({
      next: (data: any) => {
        console.log('[IncomeComponent] Income added successfully via backend:', data);
        this.incomeList.push(data);
        
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
      },
      error: (error) => {
        console.error('[IncomeComponent] Error adding income:', error);
        this.errorMessage = 'Failed to add income. Please try again.';
      }
    });
  }

  deleteIncome(id) {
    console.log('[IncomeComponent] deleteIncome called for id:', id);
    if (confirm('Are you sure you want to delete this income record?')) {
      const token = localStorage.getItem('token');
      const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
      
      this.http.delete(`${this.apiUrl}/income/${id}`, { headers }).subscribe({
        next: () => {
          console.log('[IncomeComponent] Income deleted successfully via backend');
          this.incomeList = this.incomeList.filter(income => income.id !== id);
        },
        error: (error) => {
          console.error('[IncomeComponent] Error deleting income:', error);
          alert('Failed to delete income. Please try again.');
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
}
