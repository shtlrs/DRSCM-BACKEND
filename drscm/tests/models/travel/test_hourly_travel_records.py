from rest_framework.test import APITestCase
from drscm.tests.helpers.travel import create_random_hourly_travel
from drscm.models import HourlyTravel
from drscm.tests.helpers import (
    create_random_user,
    create_random_client,
    create_random_project,
)


class HourlyTravelModelTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = create_random_user(save=True)
        cls.client_ = create_random_client(owner=cls.owner, save=True)
        cls.project = create_random_project(client=cls.client_, save=True)
        cls.travel = create_random_hourly_travel(project=cls.project)

    def test_create_fixed_travel_record(self):
        self.travel.save()
        travels = HourlyTravel.objects.all()
        self.assertEqual(len(travels), 1)

    def test_patch_fixed_travel_record(self):
        self.travel.save()
        new_hours = self.travel.hours + 1
        new_timestamp = float(self.travel.timestamp + 200)
        new_project = create_random_project(client=self.client_, save=True)

        self.travel.hours = new_hours
        self.travel.project = new_project
        self.travel.timestamp = new_timestamp
        self.travel.save()

        travel = HourlyTravel.objects.all().first()
        self.assertEqual(travel.hours, new_hours)
        self.assertEqual(float(travel.timestamp), new_timestamp)
        self.assertEqual(travel.project, new_project)

    def test_delete_fixed_travel_record(self):
        self.travel.save()
        travels = HourlyTravel.objects.all()
        self.assertEqual(len(travels), 1)
        self.travel.delete()
        travels = HourlyTravel.objects.all()
        self.assertEqual(len(travels), 0)
