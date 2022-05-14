import { Component, OnInit } from '@angular/core';
import { ClientsService } from "@clients/services/clients.service";
import {Client} from "@clients/models/client";
import {tap} from "rxjs";
import {Router} from "@angular/router";

@Component({
  selector: 'app-clients',
  templateUrl: './clients.component.html',
  styleUrls: ['./clients.component.css']
})
export class ClientsComponent implements OnInit {

  clients: Array<Client> = [];
  clientsToDisplay: Array<Client> = [];
  constructor(private clientService: ClientsService, private router: Router) { }

  ngOnInit(): void {
    this.clientService.getClients().subscribe(
      clients => (this.clients = clients) && (this.clientsToDisplay = clients)
    );
  }

  filter(event: any){
    const val = event.target.value.toLowerCase();
    this.clientsToDisplay = this.clients.filter(client => client.name.toLowerCase().includes(val));
  }

  openAddClientForm(){
    this.router.navigate(["clients/add"]);
  }

}
