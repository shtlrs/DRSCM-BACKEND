from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from drscm.serializers.user import UserSerializer
from drscm.tests.helpers import create_random_user
from drscm.views.user import ListUsersView

class UserViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = create_random_user(save=True, is_superuser=True)
        cls.user1 = create_random_user(save=True)
        cls.user2 = create_random_user(save=True)
        cls.superuser_token = RefreshToken.for_user(cls.superuser)
        cls.user1_token = RefreshToken.for_user(cls.user1)
        cls.user2_token = RefreshToken.for_user(cls.user2)


    def test_list_appropriate_users(self):
        url = reverse(ListUsersView.view_name)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.superuser_token.access_token}")

        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = UserSerializer(data=response.json(), many=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.validated_data), 3)

        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.user1_token.access_token}")

        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = UserSerializer(data=response.json(), many=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.validated_data), 0)
