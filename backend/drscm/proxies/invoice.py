from drscm.models import Invoice


class InvoiceProxy(Invoice):
    class Meta:
        proxy = True

    def get_total(self):
        fixed_travel_total = sum(
            [fixed_rate.get_total() for fixed_rate in self.fixed_travels.all()]
        )
        hourly_travel_total = sum(
            [fixed_rate.get_total() for fixed_rate in self.hourly_travels.all()]
        )
        work_sessions_total = sum(
            [work_session.get_total() for work_session in self.work_sessions.all()]
        )

        return fixed_travel_total + hourly_travel_total + work_sessions_total
