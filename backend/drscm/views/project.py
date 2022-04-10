from drscm.models import Project
from drscm.serializers.project import ProjectSerializer
from rest_framework import generics


class ProjectsList(generics.ListAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


