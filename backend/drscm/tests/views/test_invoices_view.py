from datetime import datetime

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from drscm.views import InvoiceDetailsView, CreateAndListInvoicesView
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from drscm.models import WorkSession, Invoice
from drscm.serializers import InvoiceSerializer
from utils.date import date_time_to_timestamp
from drscm.tests.helpers import (
    create_random_user,
    create_random_client,
    create_random_project,
    create_random_hourly_travel,
    create_random_fixed_travel,
    create_random_invoice,
)


class InvoiceViewTests(APITestCase):


    @classmethod
    def setUpTestData(cls):
        cls.superowner = create_random_user(is_superuser=True, save=True)
        cls.client_ = create_random_client(owner=cls.superowner, save=True)
        cls.project = create_random_project(client=cls.client_, save=True, hourly_rate=120)
        now = datetime.now()
        cls.ws1_start = date_time_to_timestamp(now.replace(hour=20, minute=30))
        cls.ws1_end = date_time_to_timestamp(now.replace(hour=21, minute=45))
        cls.ws2_start = date_time_to_timestamp(now.replace(hour=15, minute=12))
        cls.ws2_end = date_time_to_timestamp(now.replace(hour=17, minute=15))
        cls.work_session1 = WorkSession(
            project=cls.project, start_timestamp=cls.ws1_start, end_timestamp=cls.ws1_end
        )
        cls.work_session2 = WorkSession(
            project=cls.project, start_timestamp=cls.ws2_start, end_timestamp=cls.ws2_end
        )
        cls.fixed_travel = create_random_fixed_travel(project=cls.project, save=True)
        cls.hourly_travel = create_random_hourly_travel(project=cls.project, save=True)
        cls.super_token = RefreshToken.for_user(cls.superowner)

    def setUp(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.super_token.access_token}")

    def test_create_new_invoice(self):
        self.work_session2.save()
        self.work_session1.save()
        url = reverse(CreateAndListInvoicesView.view_name)
        invoice = create_random_invoice(
            project=self.project,
            work_sessions=[self.work_session1, self.work_session2],
            fixed_travels=[self.fixed_travel],
            hourly_travels=[self.hourly_travel],
        )
        invoice.owner = self.superowner
        invoice.client = self.client_
        serializer = InvoiceSerializer(instance=invoice)
        response = self.client.post(path=url, data=serializer.data)
        """
        We're setting the relation to an empty one here because during fixture teardown
        Django uses the flush command which doesn't cascade deletions but just tries to delete everything
        """
        invoice.work_sessions.set([])
        invoice.save()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_new_invoice_with_no_project(self):
        self.fail()

    def test_invoice_total(self):
        self.fail()

    def test_patch_invoice_work_sessions(self):
        self.fail()

    def test_patch_invoice_hourly_travel_sessions(self):
        self.fail()

    def test_patch_invoice_fixed_travel_sessions(self):
        self.fail()

    def test_delete_invoice(self):
        self.fail()

    def test_delete_invoice_work_sessions(self):
        self.fail()

    def test_delete_invoice_fixed_travel_sessions(self):
        self.fail()

    def test_delete_invoice_hourly_travel_sessions(self):
        self.fail()
