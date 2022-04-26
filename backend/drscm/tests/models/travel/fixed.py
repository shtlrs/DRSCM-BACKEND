from rest_framework.test import APITestCase
from drscm.tests.helpers.travel import create_random_fixed_travel
from drscm.models import FixedTravel
from drscm.tests.helpers import create_random_user, create_random_client, create_random_project


class FixedModelTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.owner = create_random_user(save=True)
        cls.client_ = create_random_client(owner=cls.owner, save=True)
        cls.project = create_random_project(client=cls.client_, save=True)
        cls.travel = create_random_fixed_travel(project=cls.project)

    def test_create_fixed_travel_record(self):
        self.travel.save()
        travels = FixedTravel.objects.all()
        self.assertEqual(len(travels), 1)

    def test_update_fixed_travel_record(self):
        self.travel.save()

    def test_patch_fixed_travel_record(self):
        self.travel.save()

    def test_delete_fixed_travel_record(self):
        self.travel.save()
        travels = FixedTravel.objects.all()
        self.assertEqual(len(travels), 1)
        self.travel.delete()
        travels = FixedTravel.objects.all()
        self.assertEqual(len(travels), 0)
