from drscm.models import FixedTravel


class FixedTravelProxy(FixedTravel):


    class Meta:
        proxy = True

    def get_total(self):
        rate = self.rate or self.project.travel_fixed_rate
        return rate * self.occurrences
