import uuid
from datetime import datetime, date

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from backend.settings.base import TEMP_DIR, TEST_FILES_DIR
import aspose.words as aw

from drscm.proxies import (
    InvoiceProxy,
    WorkSessionProxy,
    FixedTravelProxy,
    HourlyTravelProxy,
)
from drscm.views import (
    InvoiceDetailsView,
    InvoiceReportView,
    CreateAndListInvoicesView,
    FixedTravelDetailsView,
    HourlyTravelDetailsView,
    WorkSessionDetailsView,
)
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from drscm.models import WorkSession, Invoice, FixedTravel, HourlyTravel, TaxRegulation
from drscm.serializers import (
    InvoiceSerializer,
    FixedTravelSerializer,
    HourlyTravelSerializer,
    WorkSessionSerializer,
)
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
        # data for report generation

        cls.owner_for_report = create_random_user(save=True)
        cls.client_for_report = create_random_client(
            save=True,
            owner=cls.owner_for_report,
            name="Amrou Bellalouna",
            city="Msaken",
            country="Tunisia",
            street="Taieb Mhiri",
            postal_code="4070",
        )
        cls.project_for_report = create_random_project(
            client=cls.client_for_report,
            hourly_rate=134,
            travel_fixed_rate=120,
            travel_hourly_rate=45,
            save=True,
        )
        cls.session1_for_report = WorkSession(
            project=cls.project_for_report, start_timestamp=100000, end_timestamp=101800
        )
        cls.session2_for_report = WorkSession(
            project=cls.project_for_report,
            start_timestamp=102000,
            end_timestamp=102000 + 47 * 60,
        )
        cls.session3_for_report = WorkSession(
            project=cls.project_for_report,
            start_timestamp=104000,
            end_timestamp=104000 + 13 * 60,
        )
        cls.session4_for_report = WorkSession(
            project=cls.project_for_report,
            start_timestamp=106000,
            end_timestamp=106000 + 3 * 3600,
        )
        cls.session1_for_report.save()
        cls.session2_for_report.save()
        cls.session3_for_report.save()
        cls.session4_for_report.save()
        cls.fixed_travel1_for_report = FixedTravel(
            project=cls.project_for_report, rate=75, occurrences=1, timestamp=106000
        )
        cls.fixed_travel1_for_report.save()
        cls.fixed_travel2_for_report = FixedTravel(
            project=cls.project_for_report, occurrences=3, timestamp=107000
        )
        cls.fixed_travel2_for_report.save()
        cls.hourly_travel1_for_report = HourlyTravel(
            project=cls.project_for_report, hours=2, rate=30, timestamp=108000
        )
        cls.hourly_travel1_for_report.save()
        cls.hourly_travel2_for_report = HourlyTravel(
            project=cls.project_for_report, hours=1.5, timestamp=109000
        )
        cls.hourly_travel2_for_report.save()

    def setUp(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.super_token.access_token}")

    def test_create_new_invoice(self):
        self.work_session1.save()
        self.work_session2.save()
        url = reverse(CreateAndListInvoicesView.view_name)
        data = {
            "client": self.client_.id,
            "owner": self.superowner.id,
            "project": self.project.id,
            "work_sessions": [self.work_session1.id, self.work_session2.id],
            "fixed_travels": [self.fixed_travel.id],
            "hourly_travels": [self.hourly_travel.id],
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_new_invoice_with_no_project(self):
        url = reverse(CreateAndListInvoicesView.view_name)
        invoice = create_random_invoice()
        invoice.owner = self.superowner
        invoice.client = self.client_
        serializer = InvoiceSerializer(instance=invoice)
        response = self.client.post(
            path=url, data=serializer.data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_invoice_total(self):
        self.work_session1.save()
        self.work_session2.save()
        ws1_proxy = WorkSessionProxy.objects.get(pk=self.work_session1.id)
        ws2_proxy = WorkSessionProxy.objects.get(pk=self.work_session2.id)
        fixed_travel_proxy = FixedTravelProxy.objects.get(pk=self.fixed_travel.id)
        hourly_travel_proxy = HourlyTravelProxy.objects.get(pk=self.hourly_travel.id)
        data = {
            "client": self.client_.id,
            "owner": self.superowner.id,
            "project": self.project.id,
            "work_sessions": [self.work_session1.id, self.work_session2.id],
            "fixed_travels": [self.fixed_travel.id],
            "hourly_travels": [self.hourly_travel.id],
        }
        url = reverse(CreateAndListInvoicesView.view_name)
        self.client.post(path=url, data=data)

        invoice = (
            InvoiceProxy.objects.filter(
                work_sessions__in=[self.work_session1, self.work_session2]
            )
            .distinct()
            .first()
        )
        self.assertEqual(
            invoice.get_total(),
            ws1_proxy.get_total()
            + ws2_proxy.get_total()
            + fixed_travel_proxy.get_total()
            + hourly_travel_proxy.get_total(),
        )

    def _post_teardown(self):
        super(InvoiceViewTests, self)._post_teardown()

    def test_patch_invoice_work_sessions(self):
        self.work_session1.save()
        self.work_session2.save()
        new_invoice = create_random_invoice(
            project=self.project,
            work_sessions=[self.work_session1, self.work_session2],
            save=True,
        )
        new_timestamp = self.work_session1.start_timestamp - 100
        self.work_session1.start_timestamp = new_timestamp
        url = reverse(WorkSessionDetailsView.view_name, args=[self.work_session1.id])
        serializer = WorkSessionSerializer(instance=self.work_session1)
        response = self.client.patch(path=url, data=serializer.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        invoice = Invoice.objects.get(pk=new_invoice.id)
        invoice_session1 = invoice.work_sessions.get(pk=self.work_session1.id)
        self.assertEqual(new_timestamp, invoice_session1.start_timestamp)

    def test_patch_invoice_hourly_travel_sessions(self):
        new_invoice = create_random_invoice(
            project=self.project, hourly_travels=[self.hourly_travel], save=True
        )
        new_hours = self.hourly_travel.hours - 1
        self.hourly_travel.hours = new_hours
        serializer = HourlyTravelSerializer(instance=self.hourly_travel)
        url = reverse(HourlyTravelDetailsView.view_name, args=[self.hourly_travel.id])
        response = self.client.patch(path=url, data=serializer.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        invoice = Invoice.objects.get(pk=new_invoice.id)
        self.assertEqual(1, len(invoice.hourly_travels.all()))
        self.assertEqual(new_hours, invoice.hourly_travels.first().hours)

    def test_patch_invoice_fixed_travel_sessions(self):
        new_invoice = create_random_invoice(
            project=self.project, fixed_travels=[self.fixed_travel], save=True
        )
        new_occurrences = self.fixed_travel.occurrences - 1
        self.fixed_travel.occurrences = new_occurrences
        serializer = FixedTravelSerializer(instance=self.fixed_travel)
        url = reverse(FixedTravelDetailsView.view_name, args=[self.fixed_travel.id])
        response = self.client.patch(path=url, data=serializer.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        invoice = Invoice.objects.get(pk=new_invoice.id)
        self.assertEqual(1, len(invoice.fixed_travels.all()))
        self.assertEqual(new_occurrences, invoice.fixed_travels.first().occurrences)

    def test_delete_invoice(self):
        self.work_session1.save()
        self.work_session2.save()
        invoice = create_random_invoice(
            project=self.project,
            work_sessions=[self.work_session1, self.work_session2],
            fixed_travels=[self.fixed_travel],
            hourly_travels=[self.hourly_travel],
            save=True,
        )
        url = reverse(InvoiceDetailsView.view_name, args=[invoice.id])

        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertRaises(ObjectDoesNotExist, Invoice.objects.get, id=invoice.id)

    def test_delete_invoice_work_sessions(self):
        self.work_session1.save()
        self.work_session2.save()
        invoice = create_random_invoice(
            project=self.project,
            work_sessions=[self.work_session1, self.work_session2],
            fixed_travels=[self.fixed_travel],
            hourly_travels=[self.hourly_travel],
            save=True,
        )
        url = reverse(WorkSessionDetailsView.view_name, args=[self.work_session1.id])
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, len(invoice.work_sessions.all()))
        self.assertIn(self.work_session2, invoice.work_sessions.all())

    def test_delete_invoice_fixed_travel_sessions(self):
        self.work_session1.save()
        self.work_session2.save()
        invoice = create_random_invoice(
            project=self.project,
            work_sessions=[self.work_session1, self.work_session2],
            fixed_travels=[self.fixed_travel],
            hourly_travels=[self.hourly_travel],
            save=True,
        )
        url = reverse(FixedTravelDetailsView.view_name, args=[self.fixed_travel.id])
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, len(invoice.fixed_travels.all()))

    def test_delete_invoice_hourly_travel_sessions(self):
        self.work_session1.save()
        self.work_session2.save()
        invoice = create_random_invoice(
            project=self.project,
            work_sessions=[self.work_session1, self.work_session2],
            fixed_travels=[self.fixed_travel],
            hourly_travels=[self.hourly_travel],
            save=True,
        )
        url = reverse(HourlyTravelDetailsView.view_name, args=[self.hourly_travel.id])
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, len(invoice.hourly_travels.all()))

    def test_check_non_european_report_content(self):
        invoice = Invoice(
            project=self.project_for_report, tax_regulation=TaxRegulation.NON_EUROPEAN.value
        )
        invoice.save()
        invoice.fixed_travels.set(
            [self.fixed_travel1_for_report, self.fixed_travel2_for_report]
        )
        invoice.hourly_travels.set(
            [self.hourly_travel1_for_report, self.hourly_travel2_for_report]
        )
        invoice.work_sessions.set(
            [
                self.session1_for_report,
                self.session2_for_report,
                self.session3_for_report,
                self.session4_for_report,
            ]
        )
        invoice_proxy = InvoiceProxy.objects.get(pk=invoice.id)
        total = invoice_proxy.get_total()
        self.assertEqual(1165.5, total)
        url = reverse(InvoiceReportView.view_name, args=[invoice.id])
        self.client.get(path=url)
        target_invoice_path = TEST_FILES_DIR / "non_european_invoice.docx"
        newly_generated_invoice_path = TEMP_DIR / f"{invoice.id}-output.docx"
        generated_document = aw.Document(newly_generated_invoice_path.as_posix())
        target_document = aw.Document(target_invoice_path.as_posix())
        generated_document.compare(target_document, "user", date.today())
        revisions = generated_document.revisions
        differences = []
        creation_date = date.today().strftime("%d %B %Y")

        fields_to_ignore = ["03 May 2022", creation_date]
        for revision in revisions:
            group = revision.group
            if group and group.text not in fields_to_ignore:
                differences.append(group.text)
        self.assertEqual([], differences)

    def test_check_european_report_content(self):
        invoice = Invoice(
            project=self.project_for_report, tax_regulation=TaxRegulation.EUROPEAN.value
        )
        invoice.save()
        invoice.fixed_travels.set(
            [self.fixed_travel1_for_report, self.fixed_travel2_for_report]
        )
        invoice.hourly_travels.set(
            [self.hourly_travel1_for_report, self.hourly_travel2_for_report]
        )
        invoice.work_sessions.set(
            [
                self.session1_for_report,
                self.session2_for_report,
                self.session3_for_report,
                self.session4_for_report,
            ]
        )
        invoice_proxy = InvoiceProxy.objects.get(pk=invoice.id)
        total = invoice_proxy.get_total()
        self.assertEqual(1165.5, total)
        url = reverse(InvoiceReportView.view_name, args=[invoice.id])
        self.client.get(path=url)
        target_invoice_path = TEST_FILES_DIR / "european_invoice.docx"
        newly_generated_invoice_path = TEMP_DIR / f"{invoice.id}-output.docx"
        generated_document = aw.Document(newly_generated_invoice_path.as_posix())
        target_document = aw.Document(target_invoice_path.as_posix())
        generated_document.compare(target_document, "user", date.today())
        revisions = generated_document.revisions
        differences = []
        creation_date = date.today().strftime("%d %B %Y")

        fields_to_ignore = ["03 May 2022", creation_date]
        for revision in revisions:
            group = revision.group
            if group and group.text not in fields_to_ignore:
                differences.append(group.text)
        self.assertEqual([], differences)

    def test_check_dutch_report_content(self):
        invoice = Invoice(project=self.project_for_report)
        invoice.save()
        invoice.fixed_travels.set(
            [self.fixed_travel1_for_report, self.fixed_travel2_for_report]
        )
        invoice.hourly_travels.set(
            [self.hourly_travel1_for_report, self.hourly_travel2_for_report]
        )
        invoice.work_sessions.set(
            [
                self.session1_for_report,
                self.session2_for_report,
                self.session3_for_report,
                self.session4_for_report,
            ]
        )
        invoice_proxy = InvoiceProxy.objects.get(pk=invoice.id)
        total = invoice_proxy.get_total()
        self.assertEqual(1165.5, total)
        url = reverse(InvoiceReportView.view_name, args=[invoice.id])
        self.client.get(path=url)
        target_invoice_path = TEST_FILES_DIR / "dutch_invoice.docx"
        newly_generated_invoice_path = TEMP_DIR / f"{invoice.id}-output.docx"
        generated_document = aw.Document(newly_generated_invoice_path.as_posix())
        target_document = aw.Document(target_invoice_path.as_posix())
        generated_document.compare(target_document, "user", date.today())
        revisions = generated_document.revisions
        differences = []
        creation_date = date.today().strftime("%d %B %Y")

        fields_to_ignore = ["03 May 2022", creation_date]
        for revision in revisions:
            group = revision.group
            if group and group.text not in fields_to_ignore:
                differences.append(group.text)
        self.assertEqual([], differences)

    def test_create_invoice_report(self):
        self.work_session1.save()
        self.work_session2.save()
        invoice = create_random_invoice(
            project=self.project,
            work_sessions=[self.work_session1, self.work_session2],
            fixed_travels=[self.fixed_travel],
            hourly_travels=[self.hourly_travel],
            save=True,
        )

        url = reverse(InvoiceReportView.view_name, args=[invoice.id])
        invalid_url = reverse(InvoiceReportView.view_name, args=[uuid.uuid4()])
        response = self.client.get(path=invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        path = TEMP_DIR / f"{invoice.id}.docx"
        output_path = TEMP_DIR / f"{invoice.id}-output.docx"
        self.assertEqual(True, path.exists())
        self.assertEqual(True, output_path.exists())
