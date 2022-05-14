import { Component, OnInit } from '@angular/core';
import { ClientsService } from "@clients/services/clients.service";
import {Client} from "@clients/models/client";

@Component({
  selector: 'app-clients',
  templateUrl: './clients.component.html',
  styleUrls: ['./clients.component.css']
})
export class ClientsComponent implements OnInit {

  clients: Array<Client> = [];
  constructor(private clientService: ClientsService) { }

  ngOnInit(): void {
    this.clientService.getClients().subscribe(
      clients => this.clients = clients
    );
  }

}
