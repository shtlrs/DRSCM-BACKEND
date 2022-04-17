from drscm.models import Project
from drscm.serializers.project import ProjectSerializer
from rest_framework import generics


class ProjectsList(generics.ListAPIView):

    view_name = "create_or_list_projects"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetails(generics.RetrieveUpdateDestroyAPIView):
    view_name = "project_details"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


