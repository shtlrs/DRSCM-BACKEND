from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from drscm.models import Project
from drscm.serializers import ProjectSerializer
from drscm.tests.helpers.client import create_random_client
from drscm.tests.helpers.project import create_random_project
from drscm.views.project import CreateAndListProjectsView, ProjectDetailsView


class ProjectViewTest(APITestCase):
    """
    Tests for the Project views
    """

    def test_create_project(self):
        """
        Test creating a new project via an API call
        """
        url = reverse(CreateAndListProjectsView.view_name)

        client = create_random_client()
        client.save()

        project = create_random_project()
        project.client = client
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
        self.assertEqual(project_data, project_fetched_data)



