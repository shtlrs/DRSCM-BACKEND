from django.db.models import QuerySet
from drscm.models import Invoice, TaxRegulation
from drscm.interfaces.billable import Billable
from utils.date import seconds_to_hours_and_minutes
from .work_sessions import WorkSessionProxy
from .travel import HourlyTravelProxy, FixedTravelProxy


class InvoiceProxy(Invoice, Billable):

    fixed_travels_proxy: QuerySet[FixedTravelProxy]
    hourly_travels_proxy: QuerySet[HourlyTravelProxy]
    work_sessions_proxy: QuerySet[WorkSessionProxy]

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(InvoiceProxy, self).__init__(*args, **kwargs)
        self.fixed_travels_proxy = FixedTravelProxy.objects.filter(invoice=self).all()
        self.hourly_travels_proxy = HourlyTravelProxy.objects.filter(invoice=self).all()
        self.work_sessions_proxy = WorkSessionProxy.objects.filter(invoice=self).all()

    def get_number_of_travel_hours(self):
        total_travel_hours = sum(
            [
                hourly_travel.hours
                for hourly_travel in self.hourly_travels_proxy
            ]
        )
        return total_travel_hours

    def get_work_sessions_total_duration(self):
        total_seconds = sum(
            [
                work_session.session_duration.seconds
                for work_session in self.work_sessions_proxy
            ]
        )
        hours, minutes = seconds_to_hours_and_minutes(total_seconds)
        return f"{hours:02}:{minutes:02}"

    def get_work_sessions_total(self):
        work_sessions_total = sum(
            [work_session.get_total() for work_session in self.work_sessions_proxy]
        )
        return work_sessions_total

    def get_extra_travel_costs(self):
        extra_costs = 0
        extra_costs += sum(
            [fixed_travel.extra_costs for fixed_travel in self.fixed_travels_proxy]
        )

        extra_costs += sum(
            [hourly_travel.extra_costs for hourly_travel in self.hourly_travels_proxy]
        )

        return extra_costs

    def get_fixed_travels_total(self):
        fixed_travel_total = sum(
            [fixed_rate.get_total() for fixed_rate in self.fixed_travels_proxy]
        )
        return fixed_travel_total

    def get_hourly_travels_total(self):
        hourly_travel_total = sum(
            [fixed_rate.get_total() for fixed_rate in self.hourly_travels_proxy]
        )
        return hourly_travel_total

    def get_total(self):

        return (
            self.get_fixed_travels_total()
            + self.get_hourly_travels_total()
            + self.get_work_sessions_total()
        )

    def is_dutch(self):
        """
        A predicate indicating whether the invoice follows Dutch tax regulations
        """
        return self.tax_regulation == TaxRegulation.DUTCH.value

    def is_european(self):
        """
        A predicate indicating whether the invoice follows European tax regulations
        """
        return self.tax_regulation == TaxRegulation.EUROPEAN.value

    def is_non_european(self):
        """
        A predicate indicating whether the invoice follows non-European tax regulations
        """
        return self.tax_regulation == TaxRegulation.NON_EUROPEAN.value
