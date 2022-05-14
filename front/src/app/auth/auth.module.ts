import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthenticationService } from './services/authentication.service';
import { LocalStorageService } from './services/local-storage.service';
import { TokenStorageService } from './services/token-storage.service';


@NgModule({
  declarations: [
    LoginComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  exports: [LoginComponent],
  providers: [
    AuthenticationService,
    LocalStorageService,
    TokenStorageService
  ]
})
export class AuthModule { }
