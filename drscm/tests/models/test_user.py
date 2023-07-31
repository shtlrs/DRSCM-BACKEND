from django.test import TestCase
from drscm.models import User
from drscm.tests.helpers.user import create_random_user


class UserModelTests(TestCase):
    def test_create_user(self):
        user1 = create_random_user(save=True)
        user2 = create_random_user(save=True)

        users = User.objects.all()
        self.assertEqual(len(users), 2)
        self.assertIn(user1, users)
        self.assertIn(user2, users)

    def test_create_superuser(self):

        superuser = create_random_user(is_superuser=True, save=True)
        user = create_random_user(save=True)

        users = User.objects.filter(is_superuser=True)
        self.assertIn(superuser, users)
        self.assertNotIn(user, users)
        self.assertEqual(1, len(users))
