import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { ClientsComponent } from './clients/clients/clients.component';
import { DashboardComponent } from './dashboard/dashboard/dashboard.component';
import { NewClientComponent } from "@clients/forms/new-client/new-client.component";

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'clients/add', component: NewClientComponent },
  {path: 'clients', component: ClientsComponent ,
  },
  { path: 'dashboard', component: DashboardComponent },
  { path: '**', redirectTo: 'dashboard' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
