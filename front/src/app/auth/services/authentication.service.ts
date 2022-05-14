import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, tap } from 'rxjs';
import { environment } from 'src/environments/environment';
import { LocalStorageService } from './local-storage.service';
import { LoginResponse } from '../models/LoginResponse';
import { TokenStorageService } from './token-storage.service';

@Injectable({
	providedIn: 'root'
})
export class AuthenticationService {

	constructor(private http: HttpClient, private tokenStorageService: TokenStorageService) { }

	login(username: string, password: string) {
		return this.http.post<LoginResponse>(`${environment.apiUrl}/token/`, { username, password })
			.pipe(
				tap(loginResponse => {
					this.tokenStorageService.setToken(loginResponse.access);
					this.tokenStorageService.setRefreshToken(loginResponse.refresh);
				}));
	}

	refreshToken(refreshToken: string){
		return this.http.post<LoginResponse>(`${environment.apiUrl}/token/refresh`, {
			refresh: this.tokenStorageService.getRefreshToken()
		});
	}
}
