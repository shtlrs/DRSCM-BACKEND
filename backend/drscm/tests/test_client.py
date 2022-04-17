from django.test import TestCase
from drscm.models import Client
from faker import Faker

fake = Faker()


class ClientModelTests(TestCase):


    def test_add_new_client(self):
        """
        Test adding a new client
        """

        name = fake.name()
        country = fake.country()
        postal_code = fake.postcode()
        city = fake.city()
        street = fake.street_name()
        new_client = Client(name=name,
                            country=country,
                            postal_code=postal_code,
                            city=city,
                            street=street)

        client_id = new_client.id

        new_client.save()

        available_clients = Client.objects.all()

        self.assertEqual(len(available_clients), 1)

        client = Client.objects.get(id=client_id)

        self.assertEqual(client.id, client_id)
        self.assertEqual(client.name, name)
        self.assertEqual(client.country, country)
        self.assertEqual(client.postal_code, postal_code)
        self.assertEqual(client.city, city)
        self.assertEqual(client.street, street)

