import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

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

  constructor(
    private formBuilder: FormBuilder,
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

    // I Submitted 
}

}
