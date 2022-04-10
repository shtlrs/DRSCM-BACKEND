from django.urls import path
from drscm.views import ClientsList, ClientDetails, ProjectDetails, ProjectsList

urlpatterns = [
    path('clients/', ClientsList.as_view()),
    path('clients/<uuid:pk>', ClientDetails.as_view()),
    path('projects/', ProjectsList.as_view()),
    path('projects/<uuid:pk>', ProjectDetails.as_view())
]
