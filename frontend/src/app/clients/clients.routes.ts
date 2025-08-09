import { Routes } from '@angular/router';
import { ClientListComponent } from './components/client-list/client-list';
import { ClientFormComponent } from './components/client-form/client-form';

export const CLIENTS_ROUTES: Routes = [
  { path: '', component: ClientListComponent },
  {
    path: 'nuevo',
    component: ClientFormComponent,
  },
  {
    path: 'editar/:id',
    component: ClientFormComponent,
  },
];
