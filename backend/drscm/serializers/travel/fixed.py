from rest_framework import serializers
from drscm.models import FixedTravel


class HourlyTravelSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, read_only=True, allow_null=False, allow_empty=False)
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = FixedTravel
        fields = [
            "id",
            "occurrences",
            "timestamp"
            "project",
            "owner",
        ]

