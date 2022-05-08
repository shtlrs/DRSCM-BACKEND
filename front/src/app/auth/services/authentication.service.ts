import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, tap } from 'rxjs';
import { environment } from 'src/environments/environment';
import { LocalStorageService } from './local-storage.service';
import { LoginResponse } from '../models/LoginResponse';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor(private http: HttpClient, private localStorageService: LocalStorageService) { }

  login(username: string, password: string) {
    return this.http.post<LoginResponse>(`${environment.apiUrl}/users/authenticate`, { username, password }, { withCredentials: true })
        .pipe(
          tap(loginResponse => {
            this.localStorageService.setItem("token", loginResponse.accessToken);
            this.localStorageService.setItem("refreshToken", loginResponse.refreshToken);
        }));
      }
}
