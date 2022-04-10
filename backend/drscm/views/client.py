from drscm.models import Client
from drscm.serializers.client import ClientSerializer
from rest_framework import generics


class ClientsList(generics.ListAPIView):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


