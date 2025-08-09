import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { tap } from 'rxjs/operators';
import { Router } from '@angular/router';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private tokenKey = 'auth_token';
  private roleKey = 'auth_role';

  constructor(private http: HttpClient, private router: Router) {}

  login(credentials: { email: string; password: string, grant_type: string }): Observable<any> {
    return this.http.post<{ accessToken: string }>(`${this.apiUrl}/oauth/token`, credentials).pipe(
      tap((response: any) => this.setSession(response.data))
    );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.roleKey);
    this.router.navigate(['/auth/login']);
  }

  private setSession(authResult: { access_token: string, role_name: string }): void {
    localStorage.setItem(this.tokenKey, authResult.access_token);
    if (authResult.role_name) {
      localStorage.setItem(this.roleKey, authResult.role_name);
    }
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  getRole(): string | null {
    return localStorage.getItem(this.roleKey);
  }
}