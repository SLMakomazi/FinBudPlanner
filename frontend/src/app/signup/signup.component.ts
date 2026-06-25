import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  username = '';
  password = '';
  confirmPassword = '';
  errorMessage = '';
  successMessage = '';
  isLoading = false;

  router;

  constructor(router: Router, private http: HttpClient) {
    console.log('[SignupComponent] Constructor called');
    this.router = router;
  }

  ngOnInit() {
    console.log('[SignupComponent] ngOnInit called');
  }

  onSignup() {
    console.log('[SignupComponent] onSignup called', { 
      username: this.username, 
      hasPassword: !!this.password,
      hasConfirmPassword: !!this.confirmPassword 
    });
    
    if (!this.username || !this.password || !this.confirmPassword) {
      this.errorMessage = 'Please fill in all fields';
      console.log('[SignupComponent] Validation failed: missing fields');
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match';
      console.log('[SignupComponent] Validation failed: passwords do not match');
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';
    console.log('[SignupComponent] Starting signup request');

    // Call register API
    this.http.post('http://localhost:8000/api/register', {
      username: this.username,
      password: this.password
    }).subscribe({
      next: (response: any) => {
        console.log('[SignupComponent] Signup successful', response);
        this.successMessage = 'Account created successfully! Redirecting to login...';
        setTimeout(() => {
          console.log('[SignupComponent] Navigating to login');
          this.router.navigate(['/login']);
        }, 2000);
        this.isLoading = false;
      },
      error: (error) => {
        console.error('[SignupComponent] Signup failed', error);
        this.errorMessage = error.error?.detail || 'Registration failed. Please try again.';
        this.isLoading = false;
      }
    });
  }
}
