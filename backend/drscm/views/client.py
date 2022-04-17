from drscm.models import Client
from drscm.serializers.client import ClientSerializer
from rest_framework import generics


class ClientsList(generics.ListAPIView):

    view_name = "create_or_list_clients"
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetails(generics.RetrieveUpdateDestroyAPIView):

    view_name = "client_details"
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


