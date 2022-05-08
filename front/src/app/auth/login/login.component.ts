import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthenticationService } from '../services/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm?: FormGroup;
  loading = false;
  submitted = false;
  error =''

// TODO-KAREM: refresh check on send
  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthenticationService
  ) {
    // also navigate to dashboard if already logged in
  }

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  // convenience getter for easy access to form fields
  get f() { return this.loginForm!.controls; }

  onSubmit() {
    this.submitted = true;
    this.authService.login(this.f['username'].value, this.f['password'].value).pipe(

    );


}

}
