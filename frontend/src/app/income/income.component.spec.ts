import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { IncomeComponent } from './income.component';

describe('IncomeComponent', () => {
  let component: IncomeComponent;
  let fixture: ComponentFixture<IncomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [IncomeComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(IncomeComponent);
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

  it('should have incomeList property initialized as empty array', () => {
    expect(component.incomeList).toEqual([]);
  });

  it('should have newIncome object with required properties', () => {
    expect(component.newIncome).toHaveProperty('source');
    expect(component.newIncome).toHaveProperty('amount');
    expect(component.newIncome).toHaveProperty('date');
    expect(component.newIncome).toHaveProperty('category');
  });

  it('should set default date on initialization', () => {
    const today = new Date().toISOString().split('T')[0];
    expect(component.newIncome.date).toBe(today);
  });

  it('should set errorMessage when source is missing', () => {
    component.newIncome.source = '';
    component.newIncome.amount = 100;
    component.newIncome.date = '2026-01-01';
    component.newIncome.category = 'salary';
    component.onAddIncome();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set errorMessage when amount is missing', () => {
    component.newIncome.source = 'Salary';
    component.newIncome.amount = 0;
    component.newIncome.date = '2026-01-01';
    component.newIncome.category = 'salary';
    component.onAddIncome();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set errorMessage when amount is less than or equal to 0', () => {
    component.newIncome.source = 'Salary';
    component.newIncome.amount = -100;
    component.newIncome.date = '2026-01-01';
    component.newIncome.category = 'salary';
    component.onAddIncome();
    expect(component.errorMessage).toBe('Amount must be greater than 0');
  });

  it('should calculate totalMonthlyIncome correctly', () => {
    const today = new Date();
    component.incomeList = [
      { amount: 1000, date: today.toISOString(), category: 'salary' },
      { amount: 500, date: today.toISOString(), category: 'bonus' }
    ];
    expect(component.totalMonthlyIncome).toBe(1500);
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
