from rest_framework.permissions import IsAuthenticated
from drscm.models import FixedTravel
from drscm.permissions.model.is_owner import IsSuperUserOrOwner
from drscm.serializers import FixedTravelSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics


@extend_schema_view(
    get=extend_schema(
        description="Returns the list of the fixed travel available for the user",
        operation_id="List fixed travels",
    ),
    post=extend_schema(
        description="Creates a new fixed travel log for the user",
        operation_id="Create fixed travel",
    ),
)
class CreateAndListFixedTravelsView(generics.ListCreateAPIView):

    view_name = "create_or_list_fixed_travel_view"
    queryset = FixedTravel.objects.all()
    serializer_class = FixedTravelSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = FixedTravel.objects.all()
        else:
            queryset = FixedTravel.objects.filter(owner=user)

        return queryset


@extend_schema_view(
    get=extend_schema(
        description="Returns the details of a particular fixed travel",
        operation_id="Get fixed travel",
    ),
    delete=extend_schema(
        description="Deletes a particular fixed travel log",
        operation_id="Delete fixed travel",
    ),
    put=extend_schema(
        description="Updates a fixed travel fully", operation_id="Update fixed travel"
    ),
    patch=extend_schema(
        description="Patches a fixed travel by doing a partial update of specific fields",
        operation_id="Patch fixed travel",
    ),
)
class FixedTravelDetailsView(generics.RetrieveUpdateDestroyAPIView):

    view_name = "fixed_travel_details_view"
    queryset = FixedTravel.objects.all()
    serializer_class = FixedTravelSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperUserOrOwner,
    )
