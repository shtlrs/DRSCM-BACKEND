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

        owner = create_random_user(save=True)
        client = create_random_client(owner=owner, save=True)
        project = create_random_project(client=client, save=True)
        new_work_session_1 = create_random_work_session(project=project, save=True)
        new_work_session_2 = create_random_work_session(project=project, save=True)

        available_work_sessions = WorkSession.objects.all()
        self.assertEqual(len(available_work_sessions), 2)

        work_session_1: WorkSession = WorkSession.objects.get(id=new_work_session_1.id)

        self.assertEqual(work_session_1.project_id, project.id)
        self.assertEqual(work_session_1.start_timestamp, new_work_session_1.start_timestamp)
        self.assertEqual(work_session_1.end_timestamp, new_work_session_1.end_timestamp)

        work_session_2: WorkSession = WorkSession.objects.get(id=new_work_session_2.id)

        self.assertEqual(work_session_2.project_id, project.id)
        self.assertEqual(work_session_2.start_timestamp, new_work_session_2.start_timestamp)
        self.assertEqual(work_session_2.end_timestamp, new_work_session_2.end_timestamp)

    def test_delete_work_session(self):
        owner = create_random_user(save=True)
        client = create_random_client(owner=owner)
        project = create_random_project(client=client)
        work_session = create_random_work_session(project=project, save=True)

        available_work_sessions = WorkSession.objects.all()
        self.assertEqual(len(available_work_sessions), 1)

        work_session.delete()
        available_work_sessions = WorkSession.objects.all()
        self.assertEqual(len(available_work_sessions), 0)

    def test_update_work_session(self):

        new_name = "new_name"
        owner = create_random_user(save=True)
        client = create_random_client(owner=owner, save=True)
        project = create_random_project(client=client, save=True)
        new_work_session = create_random_work_session(project=project, save=True)
        work_session = WorkSession.objects.first()
        self.assertEqual(work_session.start_timestamp, new_work_session.start_timestamp)
        self.assertEqual(work_session.end_timestamp, new_work_session.end_timestamp)

        self.assertEqual(client.name, new_name)
