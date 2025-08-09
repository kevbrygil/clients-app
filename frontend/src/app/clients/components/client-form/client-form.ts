import { Component, OnInit, inject } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CommonModule, JsonPipe } from '@angular/common';

import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';

import { Client } from '../../models/client.model';
import { ClientService } from '../../services/client';
import { PersonType, PersonTypeLabel } from '../../models/person-type.enum';
import { CustomValidators } from '../../../core/validators/custom-validators';

@Component({
  selector: 'app-client-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatToolbarModule,
    MatIconModule,
  ],
  templateUrl: './client-form.html',
  styleUrl: './client-form.scss',
})
export class ClientFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private clientService = inject(ClientService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private snackBar = inject(MatSnackBar);

  form!: FormGroup;
  personTypes = Array.from(PersonTypeLabel.entries());
  isEditMode = false;
  private clientId: string | null = null;

  ngOnInit(): void {
    this.clientId = this.route.snapshot.paramMap.get('id');
    this.isEditMode = !!this.clientId;

    this.form = this.fb.group({
      company_name: ['', [Validators.required, Validators.minLength(3)]],
      person_type: [null, [Validators.required]],
      rfc: ['', [Validators.required, CustomValidators.rfc]],
      legal_representative: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      phone: ['', [Validators.required, CustomValidators.phone]],
      document: ['', [Validators.required]],
    });

    if (this.isEditMode && this.clientId) {
      this.loadClientData(this.clientId);
    }
  }

  private loadClientData(id: string): void {
    this.clientService.getClient(id).subscribe((response) => {
      this.form.patchValue(response.data);
    });
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const clientData = this.form.getRawValue();
    const saveObservable = this.isEditMode && this.clientId
      ? this.clientService.updateClient(this.clientId, clientData)
      : this.clientService.createClient(clientData);

    saveObservable.subscribe({
      next: () => {
        const message = this.isEditMode
          ? 'Cliente actualizado exitosamente.'
          : 'Cliente creado exitosamente.';
        this.snackBar.open(message, 'Cerrar', {
          duration: 3000,
          verticalPosition: 'top',
        });
        this.router.navigate(['/clientes']);
      },
      error: (err) => {
        console.error('Error al guardar el cliente', err);
        this.snackBar.open('Error al guardar el cliente. Por favor, inténtalo de nuevo.', 'Cerrar', { duration: 5000, verticalPosition: 'top', panelClass: ['error-snackbar'] });
      },
    });
  }

  onCancel(): void {
    this.router.navigate(['/clientes']);
  }
}
