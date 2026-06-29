import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ExpenseComponent } from './expense.component';

describe('ExpenseComponent', () => {
  let component: ExpenseComponent;
  let fixture: ComponentFixture<ExpenseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [ExpenseComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(ExpenseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have showAddForm property initialized as false', () => {
    expect(component.showAddForm).toBe(false);
  });

  it('should have errorMessage property initialized as empty string', () => {
    expect(component.errorMessage).toBe('');
  });

  it('should have expenseList property initialized as empty array', () => {
    expect(component.expenseList).toEqual([]);
  });

  it('should have newExpense object with required properties', () => {
    expect(component.newExpense).toHaveProperty('description');
    expect(component.newExpense).toHaveProperty('amount');
    expect(component.newExpense).toHaveProperty('date');
    expect(component.newExpense).toHaveProperty('category');
  });

  it('should set default date on initialization', () => {
    const today = new Date().toISOString().split('T')[0];
    expect(component.newExpense.date).toBe(today);
  });

  it('should set errorMessage when description is missing', () => {
    component.newExpense.description = '';
    component.newExpense.amount = 100;
    component.newExpense.date = '2026-01-01';
    component.newExpense.category = 'food';
    component.onAddExpense();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set errorMessage when amount is missing', () => {
    component.newExpense.description = 'Food';
    component.newExpense.amount = 0;
    component.newExpense.date = '2026-01-01';
    component.newExpense.category = 'food';
    component.onAddExpense();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set errorMessage when amount is less than or equal to 0', () => {
    component.newExpense.description = 'Food';
    component.newExpense.amount = -100;
    component.newExpense.date = '2026-01-01';
    component.newExpense.category = 'food';
    component.onAddExpense();
    expect(component.errorMessage).toBe('Amount must be greater than 0');
  });

  it('should calculate totalMonthlyExpenses correctly', () => {
    const today = new Date();
    component.expenseList = [
      { amount: 200, date: today.toISOString(), category: 'food' },
      { amount: 100, date: today.toISOString(), category: 'transport' }
    ];
    expect(component.totalMonthlyExpenses).toBe(300);
  });

  it('should return current month name', () => {
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December'];
    expect(months).toContain(component.currentMonth);
  });

  it('should format date correctly', () => {
    const dateString = '2026-01-15T00:00:00.000Z';
    const formatted = component.formatDate(dateString);
    expect(formatted).toContain('2026');
    expect(formatted).toContain('Jan');
  });
});
