from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from drscm.models import Project
from drscm.serializers import ProjectSerializer
from drscm.tests.helpers.client import create_random_client
from drscm.tests.helpers.project import create_random_project
from drscm.tests.helpers.user import create_random_user
from drscm.views import CreateAndListClientsView
from drscm.views import CreateAndListProjectsView, ProjectDetailsView


class ProjectViewTest(APITestCase):
    """
    Tests for the Project views
    """

    @classmethod
    def setUpTestData(cls):
        cls.owner = create_random_user()
        cls.owner.save()
        cls.token = RefreshToken.for_user(cls.owner)

    def setUp(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token.access_token}')

    def test_create_project(self):
        """
        Test creating a new project via an API call
        """
        url = reverse(CreateAndListProjectsView.view_name)

        client = create_random_client()
        client.owner = self.owner
        client.save()

        project = create_random_project()
        project.client = client
        project.owner = client.owner
        project_data = ProjectSerializer(instance=project).data

        response = self.client.post(path=url, data=project_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        available_projects = Project.objects.all()
        self.assertEqual(len(available_projects), 1)

        project_names = [available_project.name for available_project in available_projects]
        self.assertTrue(project.name in project_names)


    def test_get_all_projects_view(self):
        """
        Test getting all available project via API call
        """

        url = reverse(CreateAndListProjectsView.view_name)

        client = create_random_client()
        client.owner = self.owner
        client.save()

        first_project = create_random_project()
        first_project.client = client
        second_project = create_random_project()
        second_project.client = client
        first_project.save()
        second_project.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        project_names = [data.get('name') for data in response.json()]
        self.assertTrue(first_project.name in project_names)
        self.assertTrue(second_project.name in project_names)


    def test_get_project_by_id(self):
        """
        Tests retrieving a project by id
        """

        client = create_random_client()
        client.owner = self.owner
        client.save()

        project = create_random_project()
        project.client = client
        project.save()

        url = reverse(ProjectDetailsView.view_name, args=[project.id])
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized_project = ProjectSerializer(data=response.json())
        self.assertTrue(serialized_project.is_valid())

        project_fetched_data = serialized_project.data
        project_data = ProjectSerializer(instance=project).data
        project_data.pop('id')
        for key in project_fetched_data:
            self.assertEqual(project_data[key], project_fetched_data[key])



    def test_list_appropriate_projects_per_owner(self):
        """
        Test that projects can only be seen by their owners, unless they are admins
        """

        superuser = create_random_user(is_superuser=True)
        superuser.save()
        superuser_token = RefreshToken.for_user(superuser)
        superuser_client = create_random_client()
        superuser_client.owner = superuser
        superuser_client.save()
        superuser_project = create_random_project()
        superuser_project.client = superuser_client
        superuser_project.save()

        user = create_random_user()
        user.save()
        user_token = RefreshToken.for_user(user)
        user_client = create_random_client()
        user_client.owner = user
        user_client.save()
        user_project = create_random_project()
        user_project.client = user_client
        user_project.save()

        url = reverse(CreateAndListProjectsView.view_name)

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {superuser_token.access_token}')
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        projects = response.json()
        project_ids = [project.get('id') for project in projects]
        self.assertEqual(2, len(project_ids))
        self.assertIn(str(superuser_project.id), project_ids)
        self.assertIn(str(user_project.id), project_ids)

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {user_token.access_token}')
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        projects = response.json()
        project_ids = [project.get('id') for project in projects]
        self.assertEqual(1, len(project_ids))
        self.assertNotIn(str(superuser_project.id), project_ids)
        self.assertIn(str(user_project.id), project_ids)


    def test_query_projects_by_id_per_owner(self):
        """
        Test that projects can only be queried by their id by their owners, unless they are admins
        """
        superuser = create_random_user(is_superuser=True)
        superuser.save()
        superuser_token = RefreshToken.for_user(superuser)
        superuser_client = create_random_client()
        superuser_client.owner = superuser
        superuser_client.save()
        superuser_project = create_random_project()
        superuser_project.client = superuser_client
        superuser_project.save()

        user = create_random_user()
        user.save()
        user_token = RefreshToken.for_user(user)
        user_client = create_random_client()
        user_client.owner = user
        user_client.save()
        user_project = create_random_project()
        user_project.client = user_client
        user_project.save()

        superuser_project_url = reverse(ProjectDetailsView.view_name, args=[superuser_project.id])
        user_project_url = reverse(ProjectDetailsView.view_name, args=[user_project.id])

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {superuser_token.access_token}')

        response = self.client.get(path=superuser_project_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response = self.client.get(path=user_project_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {user_token.access_token}')
        response = self.client.get(path=superuser_project_url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        response = self.client.get(path=user_project_url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

