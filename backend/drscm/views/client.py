from rest_framework.permissions import IsAuthenticated
from drscm.models import Client
from drscm.permissions.model.is_owner import IsOwner
from drscm.serializers.client import ClientSerializer
from rest_framework import generics


class CreateAndListClientsView(generics.ListCreateAPIView):

    view_name = "create_or_list_clients_view"
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Client.objects.filter(owner=user)


class ClientDetailsView(generics.RetrieveUpdateDestroyAPIView):

    view_name = "client_details_view"
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated, IsOwner,)


