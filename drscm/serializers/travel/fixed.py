from rest_framework import serializers
from drscm.models import FixedTravel, Project


class FixedTravelSerializer(serializers.ModelSerializer):

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        many=False,
        allow_null=False,
        allow_empty=False,
    )
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = FixedTravel
        fields = [
            "id",
            "occurrences",
            "rate",
            "timestamp",
            "project",
            "owner",
        ]
