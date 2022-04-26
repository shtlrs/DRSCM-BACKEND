from rest_framework import serializers
from drscm.models import HourlyTravel


class HourlyTravelSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, read_only=True, allow_null=False, allow_empty=False)
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = HourlyTravel
        fields = [
            "id",
            "hours",
            "timestamp",
            "project",
            "owner",
        ]

