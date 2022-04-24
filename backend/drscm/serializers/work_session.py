from rest_framework import serializers
from drscm.models import WorkSession


class WorkSessionSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = WorkSession
        fields = ["id", "start_timestamp", "end_timestamp", "owner"]
