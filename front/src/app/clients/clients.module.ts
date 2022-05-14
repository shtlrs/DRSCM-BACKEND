import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ClientsComponent } from './clients/clients.component';
import { NewClientComponent } from './forms/new-client/new-client.component';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    ClientsComponent,
    NewClientComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  exports: [ClientsComponent],
})
export class ClientsModule { }
