from rest_framework.permissions import IsAuthenticated
from drscm.models import HourlyTravel
from drscm.permissions.model.is_owner import IsSuperUserOrOwner
from drscm.serializers import HourlyTravelSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics


@extend_schema_view(
    get=extend_schema(
        description="Returns the list of the hourly travel logs available for the user",
        operation_id="List hourly travels",
    ),
    post=extend_schema(
        description="Creates a new hourly travel log for the user", operation_id="Create hourly travel"
    ),
)
class CreateAndListHourlyTravelsView(generics.ListCreateAPIView):

    view_name = "create_or_list_hourly_travel_view"
    queryset = HourlyTravel.objects.all()
    serializer_class = HourlyTravelSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = HourlyTravel.objects.all()
        else:
            queryset = HourlyTravel.objects.filter(owner=user)

        return queryset


@extend_schema_view(
    get=extend_schema(
        description="Returns the details of a particular hourly travel", operation_id="Get hourly travel"
    ),
    delete=extend_schema(
        description="Deletes a particular hourly travel log", operation_id="Delete hourly travel"
    ),
    put=extend_schema(description="Updates an hourly travel fully", operation_id="Update hourly travel"),
    patch=extend_schema(
        description="Patches an hourly travel by doing a partial update of specific fields",
        operation_id="Patch hourly travel",
    ),
)
class HourlyTravelDetailsView(generics.RetrieveUpdateDestroyAPIView):

    view_name = "hourly_travel_details_view"
    queryset = HourlyTravel.objects.all()
    serializer_class = HourlyTravelSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperUserOrOwner,
    )
