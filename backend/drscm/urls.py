from django.urls import path
from drscm.views import ClientsList, ClientDetails

urlpatterns = [
    path('clients/', ClientsList.as_view()),
    path('clients/<uuid:pk>', ClientDetails.as_view())
]
