import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { BudgetComponent } from './budget.component';

describe('BudgetComponent', () => {
  let component: BudgetComponent;
  let fixture: ComponentFixture<BudgetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [BudgetComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(BudgetComponent);
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

  it('should have budgetList property initialized as empty array', () => {
    expect(component.budgetList).toEqual([]);
  });

  it('should have newBudget object with required properties', () => {
    expect(component.newBudget.category).toBeDefined();
    expect(component.newBudget.limit).toBeDefined();;
  });

  it('should set errorMessage when category is missing', () => {
    component.newBudget.category = '';
    component.newBudget.limit = 1000;
    component.onAddBudget();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set errorMessage when limit is missing', () => {
    component.newBudget.category = 'Food';
    component.newBudget.limit = 0;
    component.onAddBudget();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set errorMessage when limit is less than or equal to 0', () => {
    component.newBudget.category = 'Food';
    component.newBudget.limit = -100;
    component.onAddBudget();
    expect(component.errorMessage).toBe('Limit must be greater than 0');
  });

  it('should calculate totalBudget correctly', () => {
    component.budgetList = [
      { category: 'Food', limit: 1000 },
      { category: 'Transport', limit: 500 }
    ];
    expect(component.totalBudget).toBe(1500);
  });

  it('should calculate totalSpent correctly', () => {
    component.budgetList = [
      { category: 'Food', limit: 1000, spent: 800 },
      { category: 'Transport', limit: 500, spent: 200 }
    ];
    expect(component.totalSpent).toBe(1000);
  });

  it('should calculate remainingBudget correctly', () => {
    component.budgetList = [
      { category: 'Food', limit: 1000, spent: 800 },
      { category: 'Transport', limit: 500, spent: 200 }
    ];
    expect(component.remainingBudget).toBe(500);
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
