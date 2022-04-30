from drscm.models import Invoice
from drscm.interfaces.billable import Billable
from .work_sessions import WorkSessionProxy
from .travel import HourlyTravelProxy, FixedTravelProxy


class InvoiceProxy(Invoice, Billable):

    class Meta:
        proxy = True

    def get_total(self):
        fixed_travels = FixedTravelProxy.objects.filter(invoice=self).all()
        fixed_travel_total = sum([fixed_rate.get_total() for fixed_rate in fixed_travels])
        hourly_travels = HourlyTravelProxy.objects.filter(invoice=self).all()
        hourly_travel_total = sum([fixed_rate.get_total() for fixed_rate in hourly_travels])
        work_sessions = WorkSessionProxy.objects.filter(invoice=self).all()
        work_sessions_total = sum(
            [work_session.get_total() for work_session in work_sessions]
        )
        return fixed_travel_total + hourly_travel_total + work_sessions_total