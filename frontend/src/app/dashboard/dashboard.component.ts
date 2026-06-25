import { Component, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Chart } from 'chart.js/auto';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements AfterViewInit {
  currentUser = '';
  incomeList = [];
  expenseList = [];
  budgetList = [];

  router;
  http;
  pieChart;
  lineChart;
  selectedTab = 'week'; // 'week', 'month', 'year'
  apiUrl = ['http://127.0.0.1:8000/api','http://localhost:8000/api'];
  

  constructor(router: Router, http: HttpClient) {
    console.log('[DashboardComponent] Constructor called');
    this.router = router;
    this.http = http;
    this.loadUserData();
  }

  ngOnInit() {
    console.log('[DashboardComponent] ngOnInit called');
  }

  ngAfterViewInit() {
    console.log('[DashboardComponent] ngAfterViewInit called - initializing charts');
    this.initCharts();
  }

  selectTab(tab: string) {
    console.log('[DashboardComponent] selectTab called:', tab);
    this.selectedTab = tab;
    this.initLineChart(); // Reinitialize chart with new data
  }

  loadUserData() {
    console.log('[DashboardComponent] loadUserData called');
    const user = localStorage.getItem('currentUser');
    console.log('[DashboardComponent] User from localStorage:', user);
    if (user) {
      this.currentUser = JSON.parse(user).username;
      console.log('[DashboardComponent] Current user:', this.currentUser);
    } else {
      console.log('[DashboardComponent] No user found, navigating to login');
      this.router.navigate(['/login']);
    }

    // Load data from backend
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    
    this.http.get(`${this.apiUrl[0]}/income`, { headers }).subscribe({
      next: (data: any) => {
        this.incomeList = data;
        console.log('[DashboardComponent] Loaded income data:', this.incomeList.length, 'items from backend');
      },
      error: (error) => {
        console.error('[DashboardComponent] Error loading income data:', error);
      }
    });

    this.http.get(`${this.apiUrl[0]}/expense`, { headers }).subscribe({
      next: (data: any) => {
        this.expenseList = data;
        console.log('[DashboardComponent] Loaded expense data:', this.expenseList.length, 'items from backend');
      },
      error: (error) => {
        console.error('[DashboardComponent] Error loading expense data:', error);
      }
    });

    this.http.get(`${this.apiUrl[0]}/budget`, { headers }).subscribe({
      next: (data: any) => {
        this.budgetList = data;
        console.log('[DashboardComponent] Loaded budget data:', this.budgetList.length, 'items from backend');
      },
      error: (error) => {
        console.error('[DashboardComponent] Error loading budget data:', error);
      }
    });
  }

  updateBudgetSpending() {
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    
    this.budgetList = this.budgetList.map(budget => {
      const categoryExpenses = this.expenseList
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
  }

  get totalIncome() {
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

  get totalExpenses() {
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

  get netBalance() {
    return this.totalIncome - this.totalExpenses;
  }

  get balanceClass() {
    return this.netBalance >= 0 ? 'positive' : 'negative';
  }

  get savingsRate() {
    if (this.totalIncome === 0) return 0;
    return ((this.totalIncome - this.totalExpenses) / this.totalIncome) * 100;
  }

  get currentMonth() {
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December'];
    return months[new Date().getMonth()];
  }

  get recentTransactions() {
    const allTransactions = [
      ...this.incomeList.map(income => ({
        ...income,
        type: 'income',
        description: income.source
      })),
      ...this.expenseList.map(expense => ({
        ...expense,
        type: 'expense'
      }))
    ];

    return allTransactions
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
      .slice(0, 5);
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
      'salary': 'Salary',
      'freelance': 'Freelance',
      'investment': 'Investment',
      'rental': 'Rental Income',
      'other': 'Other'
    };
    return categoryMap[category] || category;
  }

  formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  }

  logout() {
    localStorage.removeItem('currentUser');
    this.router.navigate(['/login']);
  }

  initCharts() {
    console.log('[DashboardComponent] initCharts called');
    try {
      console.log('[DashboardComponent] Setting timeout for chart initialization');
      setTimeout(() => {
        console.log('[DashboardComponent] Timeout fired, starting pie chart');
        this.initPieChart();
        console.log('[DashboardComponent] Pie chart done, starting line chart');
        this.initLineChart();
        console.log('[DashboardComponent] Line chart done, all charts initialized');
      }, 100);
    } catch (error) {
      console.error('[DashboardComponent] Error in initCharts:', error);
    }
  }

  initPieChart() {
    console.log('[DashboardComponent] initPieChart called');
    try {
      console.log('[DashboardComponent] Getting canvas element');
      const ctx = document.getElementById('expensePieChart') as HTMLCanvasElement;
      console.log('[DashboardComponent] Canvas element:', ctx);
      if (!ctx) {
        console.log('[DashboardComponent] Canvas element not found, skipping pie chart');
        return;
      }

      console.log('[DashboardComponent] Calculating category totals');
      const categoryTotals = {};
      const currentMonth = new Date().getMonth();
      const currentYear = new Date().getFullYear();

      this.expenseList
        .filter(expense => {
          const expenseDate = new Date(expense.date);
          return expenseDate.getMonth() === currentMonth && 
                 expenseDate.getFullYear() === currentYear;
        })
        .forEach(expense => {
          if (!categoryTotals[expense.category]) {
            categoryTotals[expense.category] = 0;
          }
          categoryTotals[expense.category] += expense.amount;
        });

      console.log('[DashboardComponent] Category totals:', categoryTotals);
      const labels = Object.keys(categoryTotals).map(cat => this.formatCategory(cat));
      const data = Object.values(categoryTotals);
      const colors = [
        '#667eea', '#764ba2', '#e74c3c', '#27ae60', 
        '#f39c12', '#3498db', '#9b59b6', '#1abc9c'
      ];

      if (this.pieChart) {
        console.log('[DashboardComponent] Destroying existing pie chart');
        this.pieChart.destroy();
      }

      console.log('[DashboardComponent] Creating new pie chart');
      this.pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: colors.slice(0, labels.length),
            borderWidth: 2,
            borderColor: '#fff'
          }]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      });
      console.log('[DashboardComponent] Pie chart created successfully');
    } catch (error) {
      console.error('[DashboardComponent] Error initializing pie chart:', error);
    }
  }

  initLineChart() {
    console.log('[DashboardComponent] initLineChart called');
    try {
      console.log('[DashboardComponent] Getting canvas element');
      const ctx = document.getElementById('trendLineChart') as HTMLCanvasElement;
      console.log('[DashboardComponent] Canvas element:', ctx);
      if (!ctx) {
        console.log('[DashboardComponent] Canvas element not found, skipping line chart');
        return;
      }

      console.log('[DashboardComponent] Calculating data for tab:', this.selectedTab);
      let labels = [];
      let incomeData = [];
      let expenseData = [];

      if (this.selectedTab === 'week') {
        const weekData = this.getWeeklyData();
        labels = weekData.labels;
        incomeData = weekData.incomeData;
        expenseData = weekData.expenseData;
      } else if (this.selectedTab === 'month') {
        const monthData = this.getMonthlyData();
        labels = monthData.labels;
        incomeData = monthData.incomeData;
        expenseData = monthData.expenseData;
      } else if (this.selectedTab === 'year') {
        const yearData = this.getYearlyData();
        labels = yearData.labels;
        incomeData = yearData.incomeData;
        expenseData = yearData.expenseData;
      }

      console.log('[DashboardComponent] Data calculated:', { labels, incomeData, expenseData });

      if (this.lineChart) {
        console.log('[DashboardComponent] Destroying existing line chart');
        this.lineChart.destroy();
      }

      console.log('[DashboardComponent] Creating new line chart');
      this.lineChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Income',
              data: incomeData,
              borderColor: '#27ae60',
              backgroundColor: 'rgba(39, 174, 96, 0.1)',
              fill: true,
              tension: 0.4
            },
            {
              label: 'Expenses',
              data: expenseData,
              borderColor: '#e74c3c',
              backgroundColor: 'rgba(231, 76, 60, 0.1)',
              fill: true,
              tension: 0.4
            }
          ]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom'
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
      console.log('[DashboardComponent] Line chart created successfully');
    } catch (error) {
      console.error('[DashboardComponent] Error initializing line chart:', error);
    }
  }

  getWeeklyData() {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const incomeData = [0, 0, 0, 0, 0, 0, 0];
    const expenseData = [0, 0, 0, 0, 0, 0, 0];

    const today = new Date();
    const currentDay = today.getDay(); // 0 = Sunday, 1 = Monday, etc.
    
    // Get Monday of current week
    const monday = new Date(today);
    monday.setDate(today.getDate() - (currentDay === 0 ? 6 : currentDay - 1));
    monday.setHours(0, 0, 0, 0);

    // Get Sunday of current week
    const sunday = new Date(monday);
    sunday.setDate(monday.getDate() + 6);
    sunday.setHours(23, 59, 59, 999);

    this.incomeList.forEach(income => {
      const incomeDate = new Date(income.date);
      if (incomeDate >= monday && incomeDate <= sunday) {
        const dayIndex = incomeDate.getDay() === 0 ? 6 : incomeDate.getDay() - 1;
        incomeData[dayIndex] += income.amount;
      }
    });

    this.expenseList.forEach(expense => {
      const expenseDate = new Date(expense.date);
      if (expenseDate >= monday && expenseDate <= sunday) {
        const dayIndex = expenseDate.getDay() === 0 ? 6 : expenseDate.getDay() - 1;
        expenseData[dayIndex] += expense.amount;
      }
    });

    return { labels: days, incomeData, expenseData };
  }

  getMonthlyData() {
    const weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
    const incomeData = [0, 0, 0, 0];
    const expenseData = [0, 0, 0, 0];

    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();

    this.incomeList.forEach(income => {
      const incomeDate = new Date(income.date);
      if (incomeDate.getMonth() === currentMonth && incomeDate.getFullYear() === currentYear) {
        const dayOfMonth = incomeDate.getDate();
        const weekIndex = Math.min(Math.floor((dayOfMonth - 1) / 7), 3);
        incomeData[weekIndex] += income.amount;
      }
    });

    this.expenseList.forEach(expense => {
      const expenseDate = new Date(expense.date);
      if (expenseDate.getMonth() === currentMonth && expenseDate.getFullYear() === currentYear) {
        const dayOfMonth = expenseDate.getDate();
        const weekIndex = Math.min(Math.floor((dayOfMonth - 1) / 7), 3);
        expenseData[weekIndex] += expense.amount;
      }
    });

    return { labels: weeks, incomeData, expenseData };
  }

  getYearlyData() {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const incomeData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    const expenseData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    const currentYear = new Date().getFullYear();

    this.incomeList.forEach(income => {
      const incomeDate = new Date(income.date);
      if (incomeDate.getFullYear() === currentYear) {
        incomeData[incomeDate.getMonth()] += income.amount;
      }
    });

    this.expenseList.forEach(expense => {
      const expenseDate = new Date(expense.date);
      if (expenseDate.getFullYear() === currentYear) {
        expenseData[expenseDate.getMonth()] += expense.amount;
      }
    });

    return { labels: months, incomeData, expenseData };
  }
}
