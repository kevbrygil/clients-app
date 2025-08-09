import { Component, OnInit, inject } from '@angular/core';
import { Observable, Subject, startWith, switchMap, tap } from 'rxjs';
import { Router } from '@angular/router';
import { AsyncPipe, CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth';
import { ClientService } from '../../services/client';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTableModule } from '@angular/material/table';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiResponse } from '../../models/api-response.model';
import { PersonType, PersonTypeLabel } from '../../models/person-type.enum';
import { ConfirmationDialogComponent } from '../../../shared/components/confirmation-dialog/confirmation-dialog.component';

@Component({
  selector: 'app-client-list',
  standalone: true,
  imports: [
    CommonModule,
    AsyncPipe,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatTableModule,
    MatDialogModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
  ],
  templateUrl: './client-list.html',
  styleUrls: ['./client-list.scss'],
})
export class ClientListComponent implements OnInit {
  private clientService = inject(ClientService);
  private authService = inject(AuthService);
  private dialog = inject(MatDialog);
  private snackBar = inject(MatSnackBar);
  private router = inject(Router);

  private readonly refreshClients$ = new Subject<void>();
  public userIsAdmin = false;

  public clients$!: Observable<ApiResponse>;
  public displayedColumns: string[] = [
    'company_name',
    'person_type',
    'rfc',
    'legal_representative',
    'email',
    'phone',
    'document',
    'actions',
  ];

  ngOnInit(): void {
    this.userIsAdmin = this.authService.getRole() === 'admin';
    this.clients$ = this.refreshClients$.pipe(
      startWith(null),
      switchMap(() => this.clientService.getClients()),
      tap(() => console.log('Lista de clientes actualizada.')),
    );
  }

  getPersonType(personType: PersonType): string {
    return PersonTypeLabel.get(personType) || 'Desconocido';
  }

  deleteClient(id: string, name: string): void {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: '400px',
      data: {
        title: 'Confirmar Eliminación',
        message: `¿Estás seguro de que deseas eliminar al cliente "${name}"?`,
      },
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.clientService.deleteClient(id).subscribe({
          next: () => {
            this.snackBar.open(
              `Cliente "${name}" eliminado exitosamente.`,
              'Cerrar',
              { duration: 3000, verticalPosition: 'top' }
            );
            this.refreshClients$.next();
          },
          error: (err) => {
            this.snackBar.open(
              `Error al eliminar el cliente "${name}". Intente de nuevo.`,
              'Cerrar',
              {
                duration: 5000,
                verticalPosition: 'top',
                panelClass: ['error-snackbar'],
              }
            );
          },
        });
      }
    });
  }

  logout(): void {
    this.authService.logout();
  }

  navigateToCreateClient(): void {
    this.router.navigate(['/clientes/nuevo']);
  }

  navigateToEditClient(id: string): void {
    this.router.navigate(['/clientes/editar', id]);
  }
}
