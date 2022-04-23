from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.views import TokenObtainPairView
from drscm.tests.helpers.user import create_random_user
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class TokenViewTest(APITestCase):

    def test_request_token_with_valid_credentials(self):

        user = create_random_user()
        user.save()

        data = {
            'username': user.username,
            'email': user.email,
            'password': user.raw_password
        }

        url = reverse(TokenObtainPairView.__name__)
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer = TokenRefreshSerializer(data=response.json())
        self.assertEqual(True, serializer.is_valid())




    def test_request_token_with_invalid_credentials(self):
        self.fail()

    def test_request_token_with_non_existing_user(self):
        self.fail()

    def test_refresh_token(self):
        self.fail()

    def test_refresh_token_with_expired_refresh_token(self):
        self.fail()

