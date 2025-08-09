import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  const headersToSet: { [name: string]: string | string[] } = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  };

  if (token) {
    headersToSet['Authorization'] = `Bearer ${token}`;
  }

  const clonedReq = req.clone({ setHeaders: headersToSet });

  return next(clonedReq);
};