import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { SignupComponent } from './signup.component';

describe('SignupComponent', () => {
  let component: SignupComponent;
  let fixture: ComponentFixture<SignupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [SignupComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(SignupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have username, password, and confirmPassword properties', () => {
    expect(component.username).toBeDefined();
    expect(component.password).toBeDefined();
    expect(component.confirmPassword).toBeDefined();
  });

  it('should have errorMessage property initialized as empty string', () => {
    expect(component.errorMessage).toBe('');
  });

  it('should have successMessage property initialized as empty string', () => {
    expect(component.successMessage).toBe('');
  });

  it('should have isLoading property initialized as false', () => {
    expect(component.isLoading).toBe(false);
  });

  it('should set errorMessage when username is missing', () => {
    component.username = '';
    component.password = 'test123';
    component.confirmPassword = 'test123';
    component.onSignup();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set errorMessage when password is missing', () => {
    component.username = 'testuser';
    component.password = '';
    component.confirmPassword = 'test123';
    component.onSignup();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set errorMessage when confirmPassword is missing', () => {
    component.username = 'testuser';
    component.password = 'test123';
    component.confirmPassword = '';
    component.onSignup();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set errorMessage when passwords do not match', () => {
    component.username = 'testuser';
    component.password = 'test123';
    component.confirmPassword = 'different';
    component.onSignup();
    expect(component.errorMessage).toBe('Passwords do not match');
  });

  it('should set isLoading to true when signup is called with valid data', () => {
    component.username = 'testuser';
    component.password = 'test123';
    component.confirmPassword = 'test123';
    component.onSignup();
    expect(component.isLoading).toBe(true);
  });

  it('should clear errorMessage when signup is called with valid data', () => {
    component.errorMessage = 'Previous error';
    component.username = 'testuser';
    component.password = 'test123';
    component.confirmPassword = 'test123';
    component.onSignup();
    expect(component.errorMessage).toBe('');
  });
});
