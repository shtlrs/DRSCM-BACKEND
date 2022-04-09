from rest_framework.serializers import ModelSerializer
from backend.drscm.models import Client


class ClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'name', 'country', 'postal_code', 'city', 'street']
