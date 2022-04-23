from django.test import TestCase
from drscm.models import Client
from drscm.tests.helpers.client import create_random_client
from drscm.tests.helpers.user import create_random_user


class ClientModelTests(TestCase):

    def test_add_new_client(self):
        """
        Test adding a new client
        """

        owner = create_random_user()
        owner.save()
        new_client = create_random_client()
        client_id = new_client.id
        new_client.owner = owner
        new_client.save()

        available_clients = Client.objects.all()
        self.assertEqual(len(available_clients), 1)

        client = Client.objects.get(id=client_id)

        self.assertEqual(client.id, client_id)
        self.assertEqual(client.name, new_client.name)
        self.assertEqual(client.country, new_client.country)
        self.assertEqual(client.postal_code, new_client.postal_code)
        self.assertEqual(client.city, new_client.city)
        self.assertEqual(client.street, new_client.street)

    def test_delete_client(self):
        """
        Test deletion of a client
        """

        owner = create_random_user()
        owner.save()

        first_client = create_random_client()
        first_client.owner = owner
        first_client.save()

        second_client = create_random_client()
        second_client.owner = owner
        second_client.save()

        available_clients = Client.objects.all()
        self.assertEqual(len(available_clients), 2)

        client = Client.objects.get(id=first_client.id)
        client.delete()

        available_clients = Client.objects.all()
        self.assertEqual(len(available_clients), 1)
        remaining_client = available_clients[0]
        self.assertEqual(remaining_client.name, second_client.name)
        self.assertEqual(remaining_client.id, second_client.id)

    def test_update_client(self):

        owner = create_random_user()
        owner.save()

        new_name = "new_name"

        first_client = create_random_client()
        first_client.owner = owner
        first_client.save()

        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)
        first_client.name = new_name
        first_client.save()

        clients = Client.objects.all()
        client = clients[0]

        self.assertEqual(client.name, new_name)
