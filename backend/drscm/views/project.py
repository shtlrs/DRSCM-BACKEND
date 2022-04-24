from rest_framework.permissions import IsAuthenticated

from drscm.models import Project
from drscm.permissions.model.is_owner import IsSuperUserOrOwner
from drscm.serializers.project import ProjectSerializer
from rest_framework import generics


class CreateAndListProjectsView(generics.ListCreateAPIView):

    view_name = "create_or_list_projects_view"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            query_set = Project.objects.all()
        else:
            query_set = Project.objects.filter(owner=user)

        return query_set


class ProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    view_name = "project_details"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsSuperUserOrOwner,)


