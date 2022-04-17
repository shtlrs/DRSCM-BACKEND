from django.urls import reverse
from rest_framework import status
from drscm.models import Client
from drscm.serializers import ClientSerializer
from drscm.tests.helpers.client import create_random_client
from drscm.views.client import CreateAndListClientsView, ClientDetailsView
from rest_framework.test import APITestCase


class ClientViewTests(APITestCase):

    def test_create_clients_view(self):
        """
        Test adding a new client via API call
        """

        url = reverse(CreateAndListClientsView.view_name)

        first_client = create_random_client()
        second_client = create_random_client()

        first_client_data = ClientSerializer(instance=first_client).data
        second_client_data = ClientSerializer(instance=second_client).data

        response = self.client.post(url, data=first_client_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, data=second_client_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        available_clients = Client.objects.all()
        self.assertEqual(len(available_clients), 2)

        client_names = [client.name for client in available_clients]
        self.assertTrue(first_client.name in client_names)
        self.assertTrue(second_client.name in client_names)

    def test_get_all_clients_view(self):
        """
        Test getting clients via API call
        """

        url = reverse(CreateAndListClientsView.view_name)

        first_client = create_random_client()
        first_client.save()
        second_client = create_random_client()
        second_client.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        client_names = [data.get('name') for data in response.json()]
        self.assertTrue(first_client.name in client_names)
        self.assertTrue(second_client.name in client_names)


    def test_get_client_by_id(self):
        """
        Tests getting a client by id via API call
        """

        client = create_random_client()
        client.save()

        url = reverse(ClientDetailsView.view_name, args=[client.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client_serializer = ClientSerializer(data=response.json())
        self.assertTrue(client_serializer.is_valid())

        fetched_client_data = client_serializer.data
        client_data = ClientSerializer(instance=client).data
        self.assertEqual(fetched_client_data, client_data)