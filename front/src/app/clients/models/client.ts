

export class Client{

  public id: string;
  public name: string;
  public country: string;
  public postal_code: string;
  public city: string;
  public street: string;

  constructor(
    name: string,
    id: string,
    country: string,
    postal_code: string,
    city: string,
    street: string) {
    this.name = name;
    this.id = id;
    this.country = country;
    this.postal_code = postal_code;
    this.city = city;
    this.street = street;
  }
}
