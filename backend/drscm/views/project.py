from drscm.models import Project
from drscm.serializers.project import ProjectSerializer
from rest_framework import generics


class CreateAndListProjectsView(generics.ListCreateAPIView):

    view_name = "create_or_list_projects_view"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    view_name = "project_details"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


