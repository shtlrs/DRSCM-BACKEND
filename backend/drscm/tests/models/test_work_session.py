from django.test import TestCase
from drscm.models import WorkSession
from drscm.tests.helpers.project import create_random_project
from drscm.tests.helpers.client import create_random_client
from drscm.tests.helpers.user import create_random_user
from drscm.tests.helpers.work_session import create_random_work_session


class WorkSessionModelTests(TestCase):
    def test_add_new_work_session(self):
        """
        Tests adding a new work session
        """

        owner = create_random_user()
        owner.save()

        client = create_random_client()
        client.owner = owner
        client.save()

        new_project = create_random_project()
        new_project.client = client
        new_project.save()

        work_session = create_random_work_session()

        available_work_sessions = WorkSession.objects.all()
        self.assertEqual(len(available_projects), 1)

        project: Project = Project.objects.get(id=project_id)

        self.assertEqual(project.name, new_project.name)
        self.assertEqual(project.id, new_project.id)
        self.assertEqual(project.hourly_rate, new_project.hourly_rate)
        self.assertEqual(project.travel_hourly_rate, new_project.travel_hourly_rate)
        self.assertEqual(project.travel_fixed_rate, new_project.travel_fixed_rate)
        self.assertEqual(project.currency, new_project.currency)
        self.assertEqual(project.client_id, client.id)

    def test_delete_work_session(self):
        owner = create_random_user()
        owner.save()

        client = create_random_client()
        client.owner = owner
        client.save()

        new_project = create_random_project()
        new_project.client = client
        new_project.save()

        available_projects = Project.objects.all()
        self.assertEqual(len(available_projects), 1)

        new_project.delete()
        available_projects = Project.objects.all()
        self.assertEqual(len(available_projects), 0)

    def test_update_work_session(self):

        new_name = "new_name"

        owner = create_random_user()
        owner.save()

        client = create_random_client()
        client.owner = owner
        client.save()

        first_project = create_random_project()
        first_project.client = client
        first_project.save()

        first_project.name = new_name
        first_project.save()

        projects = Project.objects.all()
        client = projects[0]

        self.assertEqual(client.name, new_name)
