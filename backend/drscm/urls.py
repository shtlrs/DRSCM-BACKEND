from django.urls import path
from drscm.views import CreateAndListClientsView, ClientDetailsView, ProjectDetails, ProjectsList

urlpatterns = [
    path('clients/', CreateAndListClientsView.as_view(), name=CreateAndListClientsView.view_name),
    path('clients/<uuid:pk>', ClientDetailsView.as_view(), name=ClientDetailsView.view_name),
    path('projects/', ProjectsList.as_view(), name=ProjectsList.view_name),
    path('projects/<uuid:pk>', ProjectDetails.as_view(), name=ProjectDetails.view_name)
]
