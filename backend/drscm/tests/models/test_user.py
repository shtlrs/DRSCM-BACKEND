from django.test import TestCase


class UserModelTests(TestCase):

    def test_unauthenticated_request(self):
        self.assertEqual(1, 2)

    def list_appropriate_clients_per_user(self):
        self.assertEqual(1, 2)

    def list_appropriate_projects_per_user(self):
        self.assertEqual(1, 2)
