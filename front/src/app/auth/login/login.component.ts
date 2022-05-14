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
  error = ''

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
  get formControls() { return this.loginForm!.controls; }

  onSubmit() {
    this.submitted = true;
    console.log(this.formControls);
    this.authService.login(this.formControls['username'].value, this.formControls['password'].value).subscribe(
      // Do nothing for now, TODO-KAREM: redirect url wanted to go to
    );
  }

}
