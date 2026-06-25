import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'FinBudPlanner';

  constructor() {
    console.log('[AppComponent] Constructor called');
  }

  ngOnInit() {
    console.log('[AppComponent] ngOnInit called');
  }
}
