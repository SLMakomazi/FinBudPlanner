import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { DashboardComponent } from './dashboard.component';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [DashboardComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have currentUser property initialized', () => {
    expect(component.currentUser).toBeDefined();
  });

  it('should have incomeList property initialized as empty array', () => {
    expect(component.incomeList).toEqual([]);
  });

  it('should have expenseList property initialized as empty array', () => {
    expect(component.expenseList).toEqual([]);
  });

  it('should have budgetList property initialized as empty array', () => {
    expect(component.budgetList).toEqual([]);
  });

  it('should have selectedTab property initialized as week', () => {
    expect(component.selectedTab).toBe('week');
  });

  it('should calculate totalIncome correctly', () => {
    const today = new Date();
    component.incomeList = [
      { amount: 5000, date: today.toISOString() },
      { amount: 1000, date: today.toISOString() }
    ];
    expect(component.totalIncome).toBe(6000);
  });

  it('should calculate totalExpenses correctly', () => {
    const today = new Date();
    component.expenseList = [
      { amount: 2000, date: today.toISOString() },
      { amount: 500, date: today.toISOString() }
    ];
    expect(component.totalExpenses).toBe(2500);
  });

  it('should calculate netBalance correctly', () => {
    const today = new Date();
    component.incomeList = [
      { amount: 5000, date: today.toISOString() }
    ];
    component.expenseList = [
      { amount: 2000, date: today.toISOString() }
    ];
    expect(component.netBalance).toBe(3000);
  });

  it('should return positive balanceClass for positive balance', () => {
    const today = new Date();
    component.incomeList = [
      { amount: 5000, date: today.toISOString() }
    ];
    component.expenseList = [
      { amount: 2000, date: today.toISOString() }
    ];
    expect(component.balanceClass).toBe('positive');
  });

  it('should return negative balanceClass for negative balance', () => {
    const today = new Date();
    component.incomeList = [
      { amount: 1000, date: today.toISOString() }
    ];
    component.expenseList = [
      { amount: 2000, date: today.toISOString() }
    ];
    expect(component.balanceClass).toBe('negative');
  });

  it('should calculate savingsRate correctly', () => {
    const today = new Date();
    component.incomeList = [
      { amount: 5000, date: today.toISOString() }
    ];
    component.expenseList = [
      { amount: 2000, date: today.toISOString() }
    ];
    expect(component.savingsRate).toBe(60);
  });

  it('should return current month name', () => {
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December'];
    expect(months).toContain(component.currentMonth);
  });

  it('should return recent transactions sorted by date', () => {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    component.incomeList = [
      { amount: 5000, date: yesterday.toISOString(), source: 'Salary' }
    ];
    component.expenseList = [
      { amount: 2000, date: today.toISOString(), description: 'Food' }
    ];
    
    const recent = component.recentTransactions;
    expect(recent.length).toBeGreaterThan(0);
    expect(recent[0].type).toBe('expense');
  });

  it('should select tab correctly', () => {
    component.selectTab('month');
    expect(component.selectedTab).toBe('month');
  });

  it('should format category correctly', () => {
    const formatted = component.formatCategory('food');
    expect(formatted).toBe('Food & Dining');
  });

  it('should format date correctly', () => {
    const dateString = '2026-01-15T00:00:00.000Z';
    const formatted = component.formatDate(dateString);
    expect(formatted).toContain('2026');
    expect(formatted).toContain('Jan');
  });

  it('should calculate progress percentage correctly', () => {
    const percentage = component.getProgressPercentage(800, 1000);
    expect(percentage).toBe(80);
  });

  it('should return success class for progress under 80%', () => {
    const progressClass = component.getProgressClass(700, 1000);
    expect(progressClass).toBe('success');
  });

  it('should return warning class for progress between 80% and 100%', () => {
    const progressClass = component.getProgressClass(850, 1000);
    expect(progressClass).toBe('warning');
  });

  it('should return danger class for progress at or above 100%', () => {
    const progressClass = component.getProgressClass(1000, 1000);
    expect(progressClass).toBe('danger');
  });
});
