import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { LoginComponent } from './login.component';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [LoginComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have username and password properties', () => {
    expect(component.username).toBeDefined();
    expect(component.password).toBeDefined();
  });

  it('should have errorMessage property initialized as empty string', () => {
    expect(component.errorMessage).toBe('');
  });

  it('should have isLoading property initialized as false', () => {
    expect(component.isLoading).toBe(false);
  });

  it('should set errorMessage when username is missing', () => {
    component.username = '';
    component.password = 'test123';
    component.onLogin();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set errorMessage when password is missing', () => {
    component.username = 'testuser';
    component.password = '';
    component.onLogin();
    expect(component.errorMessage).toBe('Please fill in all fields');
  });

  it('should set isLoading to true when login is called with valid data', () => {
    component.username = 'testuser';
    component.password = 'test123';
    component.onLogin();
    expect(component.isLoading).toBe(true);
  });

  it('should clear errorMessage when login is called with valid data', () => {
    component.errorMessage = 'Previous error';
    component.username = 'testuser';
    component.password = 'test123';
    component.onLogin();
    expect(component.errorMessage).toBe('');
  });
});
