from rest_framework import serializers
from drscm.models import Client


class ClientSerializer(serializers.ModelSerializer):

    projects = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, allow_null=True, allow_empty=True
    )
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "country",
            "postal_code",
            "city",
            "street",
            "projects",
            "owner",
        ]
