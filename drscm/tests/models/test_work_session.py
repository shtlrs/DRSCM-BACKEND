from datetime import datetime
from django.test import TestCase
from drscm.models import WorkSession
from drscm.proxies import WorkSessionProxy
from drscm.tests.helpers.project import create_random_project
from drscm.tests.helpers.client import create_random_client
from drscm.tests.helpers.user import create_random_user
from drscm.tests.helpers.work_session import create_random_work_session


class WorkSessionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = create_random_user(save=True)
        cls.client = create_random_client(owner=cls.owner, save=True)
        cls.project = create_random_project(client=cls.client, save=True)

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

        owner = create_random_user(save=True)
        client = create_random_client(owner=owner, save=True)
        project = create_random_project(client=client, save=True)
        new_work_session = create_random_work_session(project=project, save=True)
        work_session = WorkSession.objects.first()
        self.assertEqual(work_session.start_timestamp, new_work_session.start_timestamp)
        self.assertEqual(work_session.end_timestamp, new_work_session.end_timestamp)

        new_work_session.end_timestamp += 100
        new_work_session.save()

        work_session = WorkSession.objects.first()
        self.assertEqual(work_session.end_timestamp, new_work_session.end_timestamp)

    def test_work_session_date_string(self):
        now = datetime.now()
        #  12 minutes
        start_date = now.replace(hour=15, minute=40, second=40)
        end_date = now.replace(hour=15, minute=52, second=55)
        work_session = WorkSession(
            project=self.project,
            start_timestamp=start_date.timestamp(),
            end_timestamp=end_date.timestamp(),
        )
        work_session.save()
        proxy = WorkSessionProxy.objects.get(id=work_session.id)
        self.assertEqual("00:12", proxy.get_session_duration_date_string())
        #  1 hour & 33 minutes
        start_date = now.replace(hour=15, minute=50, second=40)
        end_date = now.replace(hour=17, minute=23, second=55)
        work_session = WorkSession(
            project=self.project,
            start_timestamp=start_date.timestamp(),
            end_timestamp=end_date.timestamp(),
        )
        work_session.save()
        proxy = WorkSessionProxy.objects.get(id=work_session.id)
        self.assertEqual("01:33", proxy.get_session_duration_date_string())
        #  2 hours
        start_date = now.replace(hour=15, minute=50, second=40)
        end_date = now.replace(hour=17, minute=50, second=40)
        work_session = WorkSession(
            project=self.project,
            start_timestamp=start_date.timestamp(),
            end_timestamp=end_date.timestamp(),
        )
        work_session.save()
        proxy = WorkSessionProxy.objects.get(id=work_session.id)
        self.assertEqual("02:00", proxy.get_session_duration_date_string())
