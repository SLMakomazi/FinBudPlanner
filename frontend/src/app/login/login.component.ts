import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';
  errorMessage = '';
  isLoading = false;

  router;

  constructor(router: Router, private http: HttpClient) {
    console.log('[LoginComponent] Constructor called');
    this.router = router;
  }

  ngOnInit() {
    console.log('[LoginComponent] ngOnInit called');
  }

  onLogin() {
    console.log('[LoginComponent] onLogin called', { username: this.username, hasPassword: !!this.password });
    
    if (!this.username || !this.password) {
      this.errorMessage = 'Please fill in all fields';
      console.log('[LoginComponent] Validation failed: missing fields');
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    console.log('[LoginComponent] Starting login request');

    // Call login API using form data
    const formData = new FormData();
    formData.append('username', this.username);
    formData.append('password', this.password);

    this.http.post('http://localhost:8000/api/token', formData).subscribe({
      next: (response: any) => {
        console.log('[LoginComponent] Login successful', response);
        // Store the JWT token
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('currentUser', JSON.stringify({ username: this.username }));
        console.log('[LoginComponent] Navigating to dashboard');
        this.router.navigate(['/dashboard']);
        this.isLoading = false;
      },
      error: (error) => {
        console.error('[LoginComponent] Login failed', error);
        if (error.status === 404) {
          this.errorMessage = 'User not found. Please sign up first.';
        } else if (error.status === 401) {
          this.errorMessage = 'Incorrect password. Please try again.';
        } else {
          this.errorMessage = error.error?.detail || 'Login failed. Please try again.';
        }
        this.isLoading = false;
      }
    });
  }
}
