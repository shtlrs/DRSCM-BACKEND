from django.urls import reverse
from rest_framework import status
from drscm.models import Client
from drscm.serializers.client import ClientSerializer
from drscm.tests.helpers.client import create_fake_client
from drscm.views.client import ClientsList
from rest_framework.test import APITestCase


class ClientViewTests(APITestCase):

    def test_get_clients_view(self):
        """
        Test adding a new client via API request
        """

        url = reverse(ClientsList.view_name)

        first_client = create_fake_client()
        first_client.save()
        second_client = create_fake_client()
        second_client.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        client_names = [data.get('name') for data in response.json()]
        self.assertTrue(first_client.name in client_names)
        self.assertTrue(second_client.name in client_names)



