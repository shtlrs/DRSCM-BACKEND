from django.urls import path
from drscm.views import CreateAndListClientsView, ClientDetailsView, ProjectDetailsView, CreateAndListProjectsView

urlpatterns = [
    path('clients/', CreateAndListClientsView.as_view(), name=CreateAndListClientsView.view_name),
    path('clients/<uuid:pk>', ClientDetailsView.as_view(), name=ClientDetailsView.view_name),
    path('projects/', CreateAndListProjectsView.as_view(), name=CreateAndListProjectsView.view_name),
    path('projects/<uuid:pk>', ProjectDetailsView.as_view(), name=ProjectDetailsView.view_name)
]
