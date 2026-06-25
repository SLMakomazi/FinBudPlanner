import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

console.log('[main.ts] Starting Angular application bootstrap');

platformBrowserDynamic().bootstrapModule(AppModule)
  .then(() => {
    console.log('[main.ts] Angular application bootstrapped successfully');
  })
  .catch(err => {
    console.error('[main.ts] Angular application bootstrap failed', err);
  });
