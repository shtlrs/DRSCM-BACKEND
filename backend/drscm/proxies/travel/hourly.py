from drscm.models import HourlyTravel
from drscm.interfaces import Billable


class HourlyTravelProxy(HourlyTravel, Billable):
    class Meta:
        proxy = True

    def get_total(self):
        rate = self.rate or self.project.travel_hourly_rate
        return rate * self.hours
