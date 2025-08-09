import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export class CustomValidators {
  static rfc(control: AbstractControl): ValidationErrors | null {
    const value = control.value;
    if (!value) {
      return null;
    }

    const rfcRegex =
      /^([A-ZÑ&]{3,4}) ?(?:- ?)?(\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])) ?(?:- ?)?([A-Z\d]{2})([A\d])$/;

    return !rfcRegex.test(value.toUpperCase()) ? { invalidRfc: true } : null;
  }

  static phone(control: AbstractControl): ValidationErrors | null {
    const value = control.value;
    if (!value) {
      return null;
    }
    const phoneRegex = /^[0-9]{10}$/;
    return !phoneRegex.test(value) ? { invalidPhone: true } : null;
  }
}

