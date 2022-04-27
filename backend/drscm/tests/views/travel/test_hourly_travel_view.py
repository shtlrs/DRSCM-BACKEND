from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from drscm.tests.helpers import (
    create_random_user,
    create_random_client,
    create_random_project,
    create_random_hourly_travel,
)


class HourlyTravelViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = create_random_user(is_superuser=True, save=True)
        cls.super_client = create_random_client(owner=cls.superuser, save=True)
        cls.super_project = create_random_project(client=cls.super_client, save=True)
        cls.super_hourly_travel = create_random_hourly_travel(
            project=cls.super_project, save=False
        )
        cls.super_token = RefreshToken.for_user(cls.superuser)

        cls.user = create_random_user(is_superuser=False, save=True)
        cls.user_client = create_random_client(owner=cls.user, save=True)
        cls.user_project = create_random_project(client=cls.user_client, save=True)
        cls.user_hourly_travel = create_random_hourly_travel(
            project=cls.user_project, save=False
        )
        cls.user_token = RefreshToken.for_user(cls.user)

    def test_add_new_hourly_travel_record(self):
        self.fail()

    def test_add_new_hourly_travel_record_with_non_existent_project(self):
        self.fail()

    def test_update_travel_record(self):
        self.fail()

    def test_patch_hourly_travel_record(self):
        self.fail()

    def test_delete_hourly_travel_record(self):
        self.fail()

    def test_list_hourly_travel_records_per_appropriate_user(self):
        self.fail()

    def test_retrieve_hourly_travel_record(self):
        self.fail()

    def test_retrieve_non_existent_hourly_travel_record(self):
        self.fail()
