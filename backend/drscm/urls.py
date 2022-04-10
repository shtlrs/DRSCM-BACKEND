from django.urls import path
from drscm.views import ClientsList, ClientDetails

urlpatterns = [
    path('clients/', ClientsList.as_view()),
    path('clients/<uuid:client_id>', ClientDetails.as_view())
]
