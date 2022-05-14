import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthenticationService } from '../services/authentication.service';
import { TokenStorageService } from '../services/token-storage.service';

@Injectable()
export class JWTInterceptor implements HttpInterceptor {

  constructor(private authService: AuthenticationService, private tokenService: TokenStorageService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const token = this.tokenService.getToken();
    if(token){
      request = this.addTokenHeader(request, token);
    }
    return next.handle(request);
  }


  private addTokenHeader(request: HttpRequest<any>, token: string) {
    return request.clone({ headers: request.headers.set("Authorization", `JWT: ${token}`) });
  }
}
