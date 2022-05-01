from django.db.models import QuerySet

from drscm.models import Invoice
from drscm.interfaces.billable import Billable
from .work_sessions import WorkSessionProxy
from .travel import HourlyTravelProxy, FixedTravelProxy


class InvoiceProxy(Invoice, Billable):

    fixed_travels: QuerySet[FixedTravelProxy]
    hourly_travels: QuerySet[HourlyTravelProxy]
    work_sessions: QuerySet[WorkSessionProxy]

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(InvoiceProxy, self).__init__(*args, **kwargs)
        self.fixed_travels = FixedTravelProxy.objects.filter(invoice=self).all()
        self.hourly_travels = HourlyTravelProxy.objects.filter(invoice=self).all()
        self.work_sessions = WorkSessionProxy.objects.filter(invoice=self).all()

    def get_work_sessions_total(self):
        work_sessions_total = sum(
            [work_session.get_total() for work_session in self.work_sessions]
        )
        return work_sessions_total

    def get_fixed_travels_total(self):
        fixed_travel_total = sum(
            [fixed_rate.get_total() for fixed_rate in self.fixed_travels]
        )
        return fixed_travel_total

    def get_hourly_travels_total(self):
        hourly_travel_total = sum(
            [fixed_rate.get_total() for fixed_rate in self.hourly_travels]
        )
        return hourly_travel_total

    def get_total(self):

        return (
            self.get_fixed_travels_total()
            + self.get_hourly_travels_total()
            + self.get_work_sessions_total()
        )
