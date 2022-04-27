from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from drscm.serializers import FixedTravelSerializer
from drscm.tests.helpers import (
    create_random_user,
    create_random_client,
    create_random_project,
    create_random_fixed_travel,
)

from drscm.views import CreateAndListFixedTravelsView


class FixedTravelViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = create_random_user(is_superuser=True, save=True)
        cls.super_client = create_random_client(owner=cls.superuser, save=True)
        cls.super_project = create_random_project(client=cls.super_client, save=True)
        cls.super_fixed_travel = create_random_fixed_travel(
            project=cls.super_project, save=False
        )
        cls.super_token = RefreshToken.for_user(cls.superuser)

        cls.user = create_random_user(is_superuser=False, save=True)
        cls.user_client = create_random_client(owner=cls.user, save=True)
        cls.user_project = create_random_project(client=cls.user_client, save=True)
        cls.user_fixed_travel = create_random_fixed_travel(
            project=cls.user_project, save=False
        )
        cls.user_token = RefreshToken.for_user(cls.user)

    def setUp(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.super_token.access_token}")

    def test_add_new_fixed_travel_record(self):
        url = reverse(CreateAndListFixedTravelsView.view_name)
        data = FixedTravelSerializer(instance=self.super_fixed_travel).data
        response = self.client.post(path=url, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_add_new_fixed_travel_record_with_non_existent_project(self):
        self.fail()

    def test_update_travel_record(self):
        self.fail()

    def test_patch_fixed_travel_record(self):
        self.fail()

    def test_delete_fixed_travel_record(self):
        self.fail()

    def test_list_fixed_travel_records_per_appropriate_user(self):
        self.fail()

    def test_retrieve_fixed_travel_record(self):
        self.fail()

    def test_retrieve_non_existent_fixed_travel_record(self):
        self.fail()
