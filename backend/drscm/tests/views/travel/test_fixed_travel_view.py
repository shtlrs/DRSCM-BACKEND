from uuid import UUID
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from drscm.models import FixedTravel
from drscm.serializers import FixedTravelSerializer
from drscm.tests.helpers import (
    create_random_user,
    create_random_client,
    create_random_project,
    create_random_fixed_travel,
)

from drscm.views import CreateAndListFixedTravelsView, FixedTravelDetailsView


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
        url = reverse(CreateAndListFixedTravelsView.view_name)
        project = create_random_project(client=self.super_client)
        fixed_travel_record = create_random_fixed_travel(project=project)
        data = FixedTravelSerializer(instance=fixed_travel_record).data
        response = self.client.post(path=url, data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {"project": [f'Invalid pk "{project.id}" - object does not exist.']},
            response.json(),
        )

    def test_patch_fixed_travel_record(self):
        self.super_fixed_travel.save()
        url = reverse(FixedTravelDetailsView.view_name, args=[self.super_fixed_travel.id])
        new_timestamp = self.super_fixed_travel.timestamp + 200
        self.super_fixed_travel.timestamp = new_timestamp
        data = FixedTravelSerializer(instance=self.super_fixed_travel).data
        response = self.client.patch(path=url, data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        fixed_travel_record = FixedTravel.objects.get(pk=self.super_fixed_travel.id)
        self.assertEqual(fixed_travel_record.timestamp, self.super_fixed_travel.timestamp)

    def test_delete_fixed_travel_record(self):
        self.super_fixed_travel.save()
        url = reverse(FixedTravelDetailsView.view_name, args=[self.super_fixed_travel.id])
        data = FixedTravelSerializer(instance=self.super_fixed_travel).data
        response = self.client.delete(path=url, data=data)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        fixed_travel_records = FixedTravel.objects.filter(owner=self.superuser)
        self.assertEqual(len(fixed_travel_records), 0)

    def test_list_fixed_travel_records_per_appropriate_user(self):
        self.super_fixed_travel.save()
        self.user_fixed_travel.save()
        url = reverse(CreateAndListFixedTravelsView.view_name)
        response = self.client.get(path=url)
        fixed_travel_ids = [
            UUID(fixed_travel.get("id")) for fixed_travel in response.json()
        ]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(fixed_travel_ids), 2)
        self.assertIn(self.super_fixed_travel.id, fixed_travel_ids)
        self.assertIn(self.user_fixed_travel.id, fixed_travel_ids)

        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.user_token.access_token}")
        response = self.client.get(path=url)
        fixed_travel_ids = [
            UUID(fixed_travel.get("id")) for fixed_travel in response.json()
        ]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(fixed_travel_ids), 1)
        self.assertNotIn(self.super_fixed_travel.id, fixed_travel_ids)
        self.assertIn(self.user_fixed_travel.id, fixed_travel_ids)

    def test_retrieve_fixed_travel_record(self):
        self.super_fixed_travel.save()

        url = reverse(FixedTravelDetailsView.view_name, args=[self.super_fixed_travel.id])
        response = self.client.get(url)
        fixed_travel = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(UUID(fixed_travel.get("id")), self.super_fixed_travel.id)

    def test_retrieve_non_existent_fixed_travel_record(self):
        url = reverse(FixedTravelDetailsView.view_name, args=[self.super_fixed_travel.id])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
