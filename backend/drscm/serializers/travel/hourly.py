from rest_framework import serializers
from drscm.models import HourlyTravel, Project


class HourlyTravelSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        many=False, allow_null=False, allow_empty=False)
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = HourlyTravel
        fields = [
            "id",
            "hours",
            "rate",
            "timestamp",
            "project",
            "owner",
        ]
