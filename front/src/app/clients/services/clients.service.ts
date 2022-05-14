import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from "../../../environments/environment";
import { urlJoin } from 'url-join-ts';
import { Observable } from "rxjs";
import { Client } from "@clients/models/client";

@Injectable({
  providedIn: 'root'
})
export class ClientsService {

  constructor(private http: HttpClient) {}

  getClients(): Observable<Array<Client>>{
    const url = urlJoin(environment.apiUrl, 'clients');
    return this.http.get<Array<Client>>(url);
  }

  getClient(id: number){

  }
}
