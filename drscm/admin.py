from django.contrib import admin
from drscm.models import (
    Client,
    Project,
    WorkSession,
    User,
    HourlyTravel,
    FixedTravel,
    Invoice,
)

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(WorkSession)
admin.site.register(HourlyTravel)
admin.site.register(FixedTravel)
admin.site.register(Invoice)
