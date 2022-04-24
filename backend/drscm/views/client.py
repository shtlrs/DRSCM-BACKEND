from rest_framework.permissions import IsAuthenticated
from drscm.models import Client
from drscm.permissions.model.is_owner import IsSuperUserOrOwner
from drscm.serializers.client import ClientSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics


@extend_schema_view(
    get=extend_schema(
        description="Returns the list of the clients available for the user",
        operation_id="List clients",
    ),
    post=extend_schema(
        description="Creates a new client for the user", operation_id="Create client"
    ),
)
class CreateAndListClientsView(generics.ListCreateAPIView):

    view_name = "create_or_list_clients_view"
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Client.objects.all()
        else:
            queryset = Client.objects.filter(owner=user)

        return queryset


@extend_schema_view(
    get=extend_schema(
        description="Returns the details of a particular client", operation_id="Get client"
    ),
    delete=extend_schema(
        description="Deletes a particular client", operation_id="Delete client"
    ),
    put=extend_schema(description="Updates a client fully", operation_id="Update client"),
    patch=extend_schema(
        description="Patches a client by doing a partial update of specific fields",
        operation_id="Patch client",
    ),
)
class ClientDetailsView(generics.RetrieveUpdateDestroyAPIView):

    view_name = "client_details_view"
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperUserOrOwner,
    )
