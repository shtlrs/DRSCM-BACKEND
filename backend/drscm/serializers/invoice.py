from rest_framework import serializers
from drscm.models import (
    Client,
    Project,
    WorkSession,
    FixedTravel,
    HourlyTravel,
    User,
    Invoice,
)


class InvoiceSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=False)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), many=False)
    work_sessions = serializers.PrimaryKeyRelatedField(
        queryset=WorkSession.objects.all(), many=True
    )
    fixed_travels = serializers.PrimaryKeyRelatedField(
        queryset=FixedTravel.objects.all(), many=True
    )
    hourly_travels = serializers.PrimaryKeyRelatedField(
        queryset=HourlyTravel.objects.all(), many=True
    )

    class Meta:
        model = Invoice
        fields = [
            "owner",
            "project",
            "client",
            "work_sessions",
            "fixed_travels",
            "hourly_travels",
        ]
