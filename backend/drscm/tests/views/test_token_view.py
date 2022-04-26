from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)
from drscm.tests.helpers.user import create_random_user


class TokenViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = create_random_user()
        cls.data = {
            "username": user.username,
            "email": user.email,
            "password": user.raw_password,
        }
        cls.user = user

    def test_request_token_with_valid_credentials(self):

        self.user.save()
        create_token_url = reverse(TokenObtainPairView.__name__)
        response = self.client.post(create_token_url, data=self.data)
        token = response.json().get("access")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        verify_token_url = reverse(TokenVerifyView.__name__)
        data = {"token": token}
        response = self.client.post(verify_token_url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_request_token_with_invalid_credentials(self):
        self.user.save()
        self.data["username"] = "invalid_username"

        create_token_url = reverse(TokenObtainPairView.__name__)
        response = self.client.post(create_token_url, data=self.data)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_request_token_with_non_existing_user(self):
        self.data["username"] = "non_existing_username"

        create_token_url = reverse(TokenObtainPairView.__name__)
        response = self.client.post(create_token_url, data=self.data)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_refresh_token(self):

        self.user.save()
        create_token_url = reverse(TokenObtainPairView.__name__)
        response = self.client.post(create_token_url, data=self.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        refresh_token = response.json().get("refresh")
        refresh_token_url = reverse(TokenRefreshView.__name__)
        data = {"refresh": refresh_token}

        response = self.client.post(refresh_token_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
