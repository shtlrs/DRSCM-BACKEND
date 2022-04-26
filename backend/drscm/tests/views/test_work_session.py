from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from drscm.models import WorkSession
from drscm.views import WorkSessionDetailsView, CreateAndListWorkSessionView
from drscm.serializers import WorkSessionSerializer
from drscm.tests.helpers import create_random_user, create_random_client
from drscm.tests.helpers import create_random_project, create_random_work_session


class WorkSessionViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = create_random_user(save=True, is_superuser=True)
        cls.user = create_random_user(save=True)
        cls.superuser_client = create_random_client(owner=cls.superuser, save=True)
        cls.superuser_project = create_random_project(
            client=cls.superuser_client, save=True
        )
        cls.superuser_work_session = create_random_work_session(
            project=cls.superuser_project, save=False
        )
        cls.superuser_token = RefreshToken.for_user(cls.superuser)

        cls.user_client = create_random_client(owner=cls.user, save=True)
        cls.user_project = create_random_project(client=cls.user_client, save=True)
        cls.user_work_session = create_random_work_session(
            project=cls.user_project, save=False
        )
        cls.user_token = RefreshToken.for_user(cls.user)

    def setUp(self) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f"JWT {self.superuser_token.access_token}"
        )

    def test_list_work_sessions_per_appropriate_user(self):
        url = reverse(CreateAndListWorkSessionView.view_name)
        superuser_work_session = create_random_work_session(
            project=self.superuser_project, save=True
        )
        user_work_session = create_random_work_session(project=self.user_project, save=True)

        response = self.client.get(path=url)
        work_sessions = response.json()
        work_session_ids = [session.get("id") for session in work_sessions]
        serializer = WorkSessionSerializer(data=work_sessions, many=True)

        self.assertEqual(True, serializer.is_valid())
        self.assertEqual(len(work_sessions), 2)
        self.assertIn(str(superuser_work_session.id), work_session_ids)
        self.assertIn(str(user_work_session.id), work_session_ids)

        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.user_token.access_token}")

        response = self.client.get(path=url)
        work_sessions = response.json()
        work_session_ids = [session.get("id") for session in work_sessions]
        serializer = WorkSessionSerializer(data=work_sessions, many=True)

        self.assertEqual(True, serializer.is_valid())
        self.assertEqual(len(work_sessions), 1)
        self.assertNotIn(str(superuser_work_session.id), work_session_ids)
        self.assertIn(str(user_work_session.id), work_session_ids)

    def test_create_work_session(self):
        url = reverse(CreateAndListWorkSessionView.view_name)
        work_session = create_random_work_session(project=self.superuser_project)
        serializer = WorkSessionSerializer(instance=work_session)

        response = self.client.post(path=url, data=serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        available_work_sessions = WorkSession.objects.all()
        self.assertEqual(len(available_work_sessions), 1)

    def test_patch_work_session(self):
        self.superuser_work_session.save()
        superuser_work_session = (
            WorkSession.objects.all().filter(owner=self.superuser).first()
        )
        self.assertEqual(
            superuser_work_session.end_timestamp, self.superuser_work_session.end_timestamp
        )
        self.assertEqual(
            superuser_work_session.start_timestamp,
            self.superuser_work_session.start_timestamp,
        )

        new_end_timestamp = superuser_work_session.end_timestamp + 10
        superuser_work_session.end_timestamp = new_end_timestamp

        data = WorkSessionSerializer(instance=superuser_work_session).data

        url = reverse(
            WorkSessionDetailsView.view_name, args=[self.superuser_work_session.id]
        )
        response = self.client.patch(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        superuser_work_session = (
            WorkSession.objects.all().filter(owner=self.superuser).first()
        )
        self.assertEqual(superuser_work_session.end_timestamp, new_end_timestamp)

    def test_delete_work_session(self):
        self.superuser_work_session.save()
        url = reverse(
            WorkSessionDetailsView.view_name, args=[self.superuser_work_session.id]
        )
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        superuser_work_session = WorkSession.objects.all()
        self.assertEqual(len(superuser_work_session), 0)
