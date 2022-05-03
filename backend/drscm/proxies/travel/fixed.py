from drscm.models import FixedTravel
from drscm.interfaces import Billable


class FixedTravelProxy(FixedTravel, Billable):
    class Meta:
        proxy = True

    def get_total(self):
        rate = self.rate or self.project.travel_fixed_rate
        return round(rate * self.occurrences, 2)
