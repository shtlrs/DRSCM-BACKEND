from django.urls import path
from drscm.views import ClientsList, ClientDetails, ProjectDetails, ProjectsList

urlpatterns = [
    path('clients/', ClientsList.as_view(), name=ClientsList.view_name),
    path('clients/<uuid:pk>', ClientDetails.as_view(), name=ClientDetails.view_name),
    path('projects/', ProjectsList.as_view(), name=ProjectsList.view_name),
    path('projects/<uuid:pk>', ProjectDetails.as_view(), name=ProjectDetails.view_name)
]
