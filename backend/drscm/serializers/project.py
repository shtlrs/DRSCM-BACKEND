from rest_framework.serializers import ModelSerializer
from drscm.models import Project


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'hourly_rate', 'travel_hourly_rate', 'travel_fixed_rate', 'currency', '']
