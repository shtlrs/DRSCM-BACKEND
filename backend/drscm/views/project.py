from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated

from drscm.models import Project
from drscm.permissions.model.is_owner import IsSuperUserOrOwner
from drscm.serializers.project import ProjectSerializer
from rest_framework import generics


@extend_schema_view(
    get=extend_schema(
        description="Returns the list of the projects available for the user",
        operation_id="List projects",
    ),
    post=extend_schema(
        description="Creates a new project for the user", operation_id="Create project"
    ),
)
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


@extend_schema_view(
    get=extend_schema(
        description="Returns the details of a particular project",
        operation_id="Get project",
    ),
    delete=extend_schema(
        description="Deletes a particular project", operation_id="Delete project"
    ),
    put=extend_schema(description="Updates a project fully", operation_id="Update project"),
    patch=extend_schema(
        description="Patches a project by doing a partial update of specific fields",
        operation_id="Patch project",
    ),
)
class ProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    view_name = "project_details"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperUserOrOwner,
    )
