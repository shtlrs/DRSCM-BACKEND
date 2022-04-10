from rest_framework import serializers
from drscm.models import Project
from drscm.models import Client


class ProjectSerializer(serializers.ModelSerializer):

    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), many=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'hourly_rate', 'travel_hourly_rate', 'travel_fixed_rate', 'currency', 'client']
