import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';


@Component({
  selector: 'app-new-client',
  templateUrl: './new-client.component.html',
  styleUrls: ['./new-client.component.css']
})
export class NewClientComponent implements OnInit {

  newClientForm = new FormGroup({
    name: new FormControl(''),
    street: new FormControl('')
  });

  constructor() { }
  ngOnInit(): void {
  }

}
