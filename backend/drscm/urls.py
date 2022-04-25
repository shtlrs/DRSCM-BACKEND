from django.urls import path
from drscm.views import ListUsersView
from drscm.views import CreateAndListClientsView, ClientDetailsView
from drscm.views import ProjectDetailsView, CreateAndListProjectsView
from drscm.views import WorkSessionDetailsView, CreateAndListWorkSessionView

urlpatterns = [
    path(
        "clients/",
        CreateAndListClientsView.as_view(),
        name=CreateAndListClientsView.view_name,
    ),
    path(
        "clients/<uuid:pk>",
        ClientDetailsView.as_view(),
        name=ClientDetailsView.view_name,
    ),
    path(
        "worksession/",
        CreateAndListWorkSessionView.as_view(),
        name=CreateAndListWorkSessionView.view_name,
    ),
    path(
        "worksession/<uuid:pk>",
        WorkSessionDetailsView.as_view(),
        name=WorkSessionDetailsView.view_name,
    ),
    path(
        "projects/",
        CreateAndListProjectsView.as_view(),
        name=CreateAndListProjectsView.view_name,
    ),
    path(
        "projects/<uuid:pk>",
        ProjectDetailsView.as_view(),
        name=ProjectDetailsView.view_name,
    ),
    path("users", ListUsersView.as_view(), name=ListUsersView.view_name),
]
