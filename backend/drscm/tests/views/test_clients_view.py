from django.urls import reverse
from rest_framework import status
from drscm.models import Client
from drscm.serializers import ClientSerializer
from drscm.tests.helpers.client import create_random_client
from drscm.tests.helpers.user import create_random_user
from drscm.views.client import CreateAndListClientsView, ClientDetailsView
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class ClientViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = create_random_user()
        cls.owner.save()
        cls.token = RefreshToken.for_user(cls.owner)

    def setUp(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.token.access_token}")

    def test_create_clients_view(self):
        """
        Test adding a new client via API call
        """

        url = reverse(CreateAndListClientsView.view_name)

        first_client = create_random_client()
        first_client.owner = self.owner
        second_client = create_random_client()
        second_client.owner = self.owner

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
        first_client.owner = self.owner
        first_client.save()
        second_client = create_random_client()
        second_client.owner = self.owner
        second_client.save()

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        client_names = [data.get("name") for data in response.json()]
        self.assertTrue(first_client.name in client_names)
        self.assertTrue(second_client.name in client_names)

    def test_get_client_by_id(self):
        """
        Tests getting a client by id via API call
        """

        client = create_random_client()
        client.owner = self.owner
        client.save()

        url = reverse(ClientDetailsView.view_name, args=[client.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        fetched_client_serializer = ClientSerializer(data=response.json())
        self.assertTrue(fetched_client_serializer.is_valid())

        fetched_client_data = fetched_client_serializer.validated_data
        client_serializer = ClientSerializer(instance=client)
        client_data = client_serializer.data

        self.assertEqual(client_data.get("projects"), [])
        self.assertEqual(client_data.get("id"), str(client.id))

        client_data.pop("id")
        client_data.pop("projects")

        for field in fetched_client_data.keys():
            self.assertEqual(fetched_client_data[field], client_data[field])

    def test_list_appropriate_clients_per_owner(self):

        superuser = create_random_user(is_superuser=True)
        superuser.save()
        superuser_token = RefreshToken.for_user(superuser)

        user = create_random_user()
        user.save()
        user_token = RefreshToken.for_user(user)

        superuser_client = create_random_client()
        superuser_client.owner = superuser
        superuser_client.save()

        user_client = create_random_client()
        user_client.owner = user
        user_client.save()

        url = reverse(CreateAndListClientsView.view_name)

        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {superuser_token.access_token}")
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        clients = response.json()
        client_ids = [client.get("id") for client in clients]
        self.assertEqual(2, len(client_ids))
        self.assertIn(str(superuser_client.id), client_ids)
        self.assertIn(str(user_client.id), client_ids)

        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {user_token.access_token}")
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        clients = response.json()
        client_ids = [client.get("id") for client in clients]
        self.assertEqual(1, len(client_ids))
        self.assertNotIn(str(superuser_client.id), client_ids)
        self.assertIn(str(user_client.id), client_ids)

    def test_query_clients_by_id_per_owner(self):
        """
        Test that clients can only be queried by their id by their owners, unless they are admins
        """
        superuser = create_random_user(is_superuser=True)
        superuser.save()
        superuser_token = RefreshToken.for_user(superuser)
        superuser_client = create_random_client()
        superuser_client.owner = superuser
        superuser_client.save()

        user = create_random_user()
        user.save()
        user_token = RefreshToken.for_user(user)
        user_client = create_random_client()
        user_client.owner = user
        user_client.save()

        superuser_client_url = reverse(
            ClientDetailsView.view_name, args=[superuser_client.id]
        )
        user_clients_url = reverse(ClientDetailsView.view_name, args=[user_client.id])

        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {superuser_token.access_token}")

        response = self.client.get(path=superuser_client_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(path=user_clients_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {user_token.access_token}")
        response = self.client.get(path=superuser_client_url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        response = self.client.get(path=user_clients_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
