from datetime import datetime
from rest_framework.test import APITestCase
from drscm.models import WorkSession, Invoice
from drscm.proxies import (
    InvoiceProxy,
    WorkSessionProxy,
    FixedTravelProxy,
    HourlyTravelProxy,
)
from utils.date import date_time_to_timestamp
from django.core.exceptions import ObjectDoesNotExist
from drscm.tests.helpers import (
    create_random_user,
    create_random_client,
    create_random_project,
    create_random_hourly_travel,
    create_random_fixed_travel,
    create_random_invoice,
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
        cls.work_session1 = WorkSession(
            project=cls.project, start_timestamp=cls.ws1_start, end_timestamp=cls.ws1_end
        )
        cls.work_session2 = WorkSession(
            project=cls.project, start_timestamp=cls.ws2_start, end_timestamp=cls.ws2_end
        )

    def test_create_new_invoice(self):
        self.work_session1.save()
        self.work_session2.save()
        invoice = create_random_invoice(
            project=self.project, work_sessions=[self.work_session1, self.work_session2]
        )
        invoices = Invoice.objects.all()
        self.assertEqual(0, len(invoices))

        invoice.save()
        invoices = Invoice.objects.all()
        self.assertEqual(1, len(invoices))

    def test_create_new_invoice_with_no_project(self):
        self.work_session1.save()
        self.work_session2.save()
        invoice = Invoice(project=None)
        self.assertRaises(ObjectDoesNotExist, invoice.save)

    def test_invoice_total(self):
        invoice_total = 0.0
        invoice = Invoice(project=self.project)
        invoice.save()
        invoice_proxy = InvoiceProxy.objects.get(pk=invoice.id)
        self.assertEqual(0, invoice_proxy.get_total())
        self.work_session1.save()
        self.work_session2.save()
        session1_proxy = WorkSessionProxy.objects.get(id=self.work_session1.id)
        session2_proxy = WorkSessionProxy.objects.get(id=self.work_session2.id)
        invoice.work_sessions.set([self.work_session1, self.work_session2])
        invoice_total += session1_proxy.get_total() + session2_proxy.get_total()
        invoice_proxy = InvoiceProxy.objects.get(pk=invoice.id)
        self.assertEqual(invoice_proxy.get_total(), invoice_total)

        fixed_travel = create_random_fixed_travel(project=self.project, save=True)
        fixed_travel_proxy = FixedTravelProxy.objects.get(id=fixed_travel.id)
        invoice_total += fixed_travel_proxy.get_total()
        invoice.fixed_travels.set([fixed_travel])
        invoice.save()
        invoice_proxy = InvoiceProxy.objects.get(pk=invoice.id)
        self.assertEqual(invoice_proxy.get_total(), invoice_total)

        hourly_travel = create_random_hourly_travel(project=self.project, save=True)
        hourly_travel_proxy = HourlyTravelProxy.objects.get(id=hourly_travel.id)
        invoice_total += hourly_travel_proxy.get_total()
        invoice.hourly_travels.set([hourly_travel])
        invoice.save()
        invoice_proxy = InvoiceProxy.objects.get(pk=invoice.id)
        self.assertEqual(invoice_proxy.get_total(), invoice_total)

    def test_patch_invoice_work_sessions(self):
        self.work_session1.save()
        create_random_invoice(
            project=self.project, work_sessions=[self.work_session1], save=True
        )
        new_time_stamp = self.work_session1.start_timestamp - 100
        self.work_session1.start_timestamp = new_time_stamp
        self.work_session1.save()
        invoice = Invoice.objects.all().first()
        self.assertEqual(1, len(invoice.work_sessions.all()))
        work_session = invoice.work_sessions.first()
        self.assertEqual(new_time_stamp, work_session.start_timestamp)

    def test_patch_invoice_hourly_travel_sessions(self):
        fixed_travel = create_random_fixed_travel(project=self.project, save=True)
        create_random_invoice(project=self.project, fixed_travels=[fixed_travel], save=True)
        new_occurrence = fixed_travel.occurrences + 2
        fixed_travel.occurrences = new_occurrence
        fixed_travel.save()
        invoice = Invoice.objects.all().first()
        self.assertEqual(1, len(invoice.fixed_travels.all()))
        invoice_fixed_travel = invoice.fixed_travels.first()
        self.assertEqual(new_occurrence, invoice_fixed_travel.occurrences)

    def test_patch_invoice_fixed_travel_sessions(self):
        hourly_travel = create_random_hourly_travel(project=self.project, save=True)
        create_random_invoice(
            project=self.project, hourly_travels=[hourly_travel], save=True
        )
        new_hours = hourly_travel.hours + 2
        hourly_travel.hours = new_hours
        hourly_travel.save()
        invoice = Invoice.objects.all().first()
        self.assertEqual(1, len(invoice.hourly_travels.all()))
        invoice_hourly_travel = invoice.hourly_travels.first()
        self.assertEqual(new_hours, invoice_hourly_travel.hours)

    def test_delete_invoice(self):
        invoice = Invoice(project=self.project)
        invoice.save()
        self.assertEqual(1, len(Invoice.objects.all()))
        invoice.delete()
        self.assertEqual(0, len(Invoice.objects.all()))

    def test_delete_invoice_work_sessions(self):
        self.work_session1.save()
        self.work_session2.save()
        new_invoice = Invoice(project=self.project)
        new_invoice.work_sessions.set([self.work_session1, self.work_session2])
        new_invoice.save()
        invoice = Invoice.objects.all().first()
        self.assertEqual(2, len(invoice.work_sessions.all()))
        new_invoice.work_sessions.set([])
        new_invoice.save()
        invoice = Invoice.objects.all().first()
        self.assertEqual(0, len(invoice.work_sessions.all()))

    def test_delete_invoice_fixed_travel_sessions(self):
        fixed_travel = create_random_fixed_travel(project=self.project, save=True)
        new_invoice = Invoice(project=self.project)
        new_invoice.fixed_travels.set([fixed_travel])
        new_invoice.save()
        invoice = Invoice.objects.all().first()
        self.assertEqual(1, len(invoice.fixed_travels.all()))
        new_invoice.fixed_travels.set([])
        new_invoice.save()
        invoice = Invoice.objects.all().first()
        self.assertEqual(0, len(invoice.fixed_travels.all()))

    def test_delete_invoice_hourly_travel_sessions(self):
        hourly_travel = create_random_hourly_travel(project=self.project, save=True)
        new_invoice = Invoice(project=self.project)
        new_invoice.hourly_travels.set([hourly_travel])
        new_invoice.save()
        invoice = Invoice.objects.all().first()
        self.assertEqual(1, len(invoice.hourly_travels.all()))
        new_invoice.hourly_travels.set([])
        new_invoice.save()
        invoice = Invoice.objects.all().first()
        self.assertEqual(0, len(invoice.hourly_travels.all()))
