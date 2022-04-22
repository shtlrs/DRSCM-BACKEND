from django.contrib import admin
from drscm.models import Client, Project, WorkSession

admin.site.register(Client)
admin.site.register(Project)
admin.site.register(WorkSession)
