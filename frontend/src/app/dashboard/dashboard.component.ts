import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  currentUser = '';
  incomeList = [];
  expenseList = [];
  budgetList = [];

  router;
  pieChart;
  lineChart;

  constructor(router: Router) {
    this.router = router;
    this.loadUserData();
    this.initCharts();
  }

  loadUserData() {
    const user = localStorage.getItem('currentUser');
    if (user) {
      this.currentUser = JSON.parse(user).username;
    } else {
      this.router.navigate(['/login']);
    }

    const incomeData = localStorage.getItem('incomeData');
    if (incomeData) {
      this.incomeList = JSON.parse(incomeData);
    }

    const expenseData = localStorage.getItem('expenseData');
    if (expenseData) {
      this.expenseList = JSON.parse(expenseData);
    }

    const budgetData = localStorage.getItem('budgetData');
    if (budgetData) {
      this.budgetList = JSON.parse(budgetData);
      this.updateBudgetSpending();
    }
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
    setTimeout(() => {
      this.initPieChart();
      this.initLineChart();
    }, 100);
  }

  initPieChart() {
    const ctx = document.getElementById('expensePieChart');
    if (!ctx) return;

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

    const labels = Object.keys(categoryTotals).map(cat => this.formatCategory(cat));
    const data = Object.values(categoryTotals);
    const colors = [
      '#667eea', '#764ba2', '#e74c3c', '#27ae60', 
      '#f39c12', '#3498db', '#9b59b6', '#1abc9c'
    ];

    if (this.pieChart) {
      this.pieChart.destroy();
    }

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
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    });
  }

  initLineChart() {
    const ctx = document.getElementById('trendLineChart');
    if (!ctx) return;

    const months = [];
    const incomeData = [];
    const expenseData = [];

    for (let i = 5; i >= 0; i--) {
      const date = new Date();
      date.setMonth(date.getMonth() - i);
      const month = date.getMonth();
      const year = date.getFullYear();
      
      months.push(date.toLocaleDateString('en-US', { month: 'short' }));

      const monthIncome = this.incomeList
        .filter(income => {
          const incomeDate = new Date(income.date);
          return incomeDate.getMonth() === month && 
                 incomeDate.getFullYear() === year;
        })
        .reduce((total, income) => total + income.amount, 0);

      const monthExpense = this.expenseList
        .filter(expense => {
          const expenseDate = new Date(expense.date);
          return expenseDate.getMonth() === month && 
                 expenseDate.getFullYear() === year;
        })
        .reduce((total, expense) => total + expense.amount, 0);

      incomeData.push(monthIncome);
      expenseData.push(monthExpense);
    }

    if (this.lineChart) {
      this.lineChart.destroy();
    }

    this.lineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: months,
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
        responsive: true,
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
  }
}
