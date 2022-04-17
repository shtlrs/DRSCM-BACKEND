from drscm.models import Client
from drscm.serializers.client import ClientSerializer
from rest_framework import generics


class CreateAndListClientsView(generics.ListCreateAPIView):

    view_name = "create_or_list_clients_view"
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetailsView(generics.RetrieveUpdateDestroyAPIView):

    view_name = "client_details_view"
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


