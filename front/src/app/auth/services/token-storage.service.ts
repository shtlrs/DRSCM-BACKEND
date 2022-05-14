import { Injectable } from '@angular/core';
import { LocalStorageService } from './local-storage.service';

@Injectable({
  providedIn: 'root'
})
export class TokenStorageService {

  constructor(private localStorage: LocalStorageService) { }

  public setToken(token: string): void {
    this.localStorage.setItem("token", token);
  }

  public setRefreshToken(refresh: string) {
    this.localStorage.setItem("refreshToken", refresh);
  }

  public getToken(): string | null {
    return this.localStorage.getItem("token");
  }

  public getRefreshToken(): string | null {
    return this.localStorage.getItem("refreshToken");
  }
}
