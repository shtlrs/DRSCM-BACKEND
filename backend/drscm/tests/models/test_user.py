from django.test import TestCase
from drscm.models import User
from drscm.tests.helpers.user import create_random_user


class UserModelTests(TestCase):

    def test_create_user(self):
        user1 = create_random_user()
        user1.save()

        user2 = create_random_user()
        user2.save()

        users = User.objects.all()
        self.assertEqual(len(users), 2)
        self.assertIn(user1, users)
        self.assertIn(user2, users)


    def test_create_superuser(self):

        superuser = create_random_user(is_superuser=True)
        superuser.save()

        user = create_random_user()
        user.save()

        users = User.objects.filter(is_superuser=True)
        self.assertIn(superuser, users)
        self.assertEqual(1, len(users))


    def list_all_clients_for_superuser(self):
        """
        Test that a super user can see all client
        """
        self.assertEqual(1, 2)

    def list_all_projects_for_superuser(self):
        """
        Test that a superuser can see all projects
        """
        self.assertEqual(1, 2)

    def list_appropriate_clients_for_user(self):
        """
        Test that each user can only see their clients
        """
        self.assertEqual(1, 2)

    def list_appropriate_projects_for_user(self):
        """
        Test that each user can only see their clients
        """
        self.assertEqual(1, 2)
