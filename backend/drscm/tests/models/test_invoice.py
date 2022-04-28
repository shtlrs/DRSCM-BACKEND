from datetime import datetime
from rest_framework.test import APITestCase
from drscm.models import WorkSession, Invoice
from utils.date import date_time_to_timestamp
from django.core.exceptions import ObjectDoesNotExist
from drscm.tests.helpers import (
    create_random_user,
    create_random_client,
    create_random_work_session,
    create_random_project,
    create_random_hourly_travel,
    create_random_fixed_travel,
)


class InvoiceModelTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.owner = create_random_user(save=True)
        cls.client_ = create_random_client(owner=cls.owner, save=True)
        cls.project = create_random_project(client=cls.client_, save=True, hourly_rate=120)
        now = datetime.now()
        cls.ws1_start = date_time_to_timestamp(now.replace(hour=20, minute=30))
        cls.ws1_end = date_time_to_timestamp(now.replace(hour=21, minute=45))
        cls.ws2_start = date_time_to_timestamp(now.replace(hour=15, minute=12))
        cls.ws2_end = date_time_to_timestamp(now.replace(hour=17, minute=15))
        cls.work_session1 = WorkSession(project=cls.project, start_timestamp=cls.ws1_start, end_timestamp=cls.ws1_end)
        cls.work_session2 = WorkSession(project=cls.project, start_timestamp=cls.ws2_start, end_timestamp=cls.ws2_end)

    def test_create_new_invoice(self):
        self.work_session1.save()
        self.work_session2.save()
        invoice = Invoice(project=self.project)
        invoice.work_sessions.set([self.work_session1, self.work_session2])
        invoices = Invoice.objects.all()
        self.assertEqual(0, len(invoices))

        invoice.save()
        invoices = Invoice.objects.all()
        self.assertEqual(1, len(invoices))

    def test_create_new_invoice_with_no_project(self):
        self.work_session1.save()
        self.work_session2.save()
        invoice = Invoice(project=None)
        invoice.work_sessions.set([self.work_session1, self.work_session2])
        self.assertRaises(invoice.related.RelatedObjectDoesNotExist, invoice.save())

    def test_create_new_invoice_with_no_work_sessions(self):
        self.fail()

    def test_create_new_invoice_with_no_fixed_travels(self):
        self.fail()

    def test_create_new_invoice_with_no_hourly_travels(self):
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
