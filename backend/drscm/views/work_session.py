from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drscm.models import WorkSession
from drscm.permissions.model.is_owner import IsSuperUserOrOwner
from drscm.serializers import WorkSessionSerializer
from rest_framework import generics, status


@extend_schema_view(
    get=extend_schema(
        description="Returns the list of the work sessions available for a project",
        operation_id="List work sessions",
    ),
    post=extend_schema(
        description="Creates a new work session of a particular project",
        operation_id="Create Worksession",
    ),
)
class CreateAndListWorkSessionView(generics.ListCreateAPIView):

    view_name = "create_or_list_worksession_view"
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            query_set = WorkSession.objects.all()
        else:
            query_set = WorkSession.objects.filter(owner=user)
        return query_set


@extend_schema_view(
    get=extend_schema(
        description="Returns the details of a particular worksession",
        operation_id="Get work session",
    ),
    delete=extend_schema(
        description="Deletes a particular work session", operation_id="Delete work session"
    ),
    put=extend_schema(
        description="Updates a work session fully", operation_id="Update work session"
    ),
    patch=extend_schema(
        description="Patches a work session by doing a partial update of specific fields",
        operation_id="Patch work session",
    ),
)
class WorkSessionDetailsView(generics.RetrieveUpdateDestroyAPIView):
    view_name = "worksession_details"
    queryset = WorkSession.objects.all()
    serializer_class = WorkSessionSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperUserOrOwner,
    )
