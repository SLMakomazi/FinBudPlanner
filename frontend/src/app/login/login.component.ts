import { Component } from '@angular/core';
import { Router } from '@angular/router';

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

  constructor(router: Router) {
    this.router = router;
  }

  onLogin() {
    if (!this.username || !this.password) {
      this.errorMessage = 'Please fill in all fields';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    // Simulate login - in production, this would call an API
    setTimeout(() => {
      // Simple validation for demo purposes
      if (this.username.length >= 3 && this.password.length >= 6) {
        localStorage.setItem('currentUser', JSON.stringify({ username: this.username }));
        this.router.navigate(['/dashboard']);
      } else {
        this.errorMessage = 'Invalid credentials. Username must be at least 3 characters and password at least 6 characters.';
      }
      this.isLoading = false;
    }, 1000);
  }
}
