import { Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: 'auth',
    loadChildren: () =>
      import('./auth/auth.routes').then((mod) => mod.AUTH_ROUTES),
  },
  {
    path: 'clientes',
    loadChildren: () =>
      import('./clients/clients.routes').then((mod) => mod.CLIENTS_ROUTES),
    canActivate: [AuthGuard],
  },
  {
    path: '',
    redirectTo: 'auth',
    pathMatch: 'full',
  },
  { path: '**', redirectTo: 'auth' },
];
