from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)



class UserViewTest(APITestCase):

    def test_list_users(self):
        self.fail()
