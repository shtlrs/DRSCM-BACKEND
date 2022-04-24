from rest_framework import serializers
from drscm.models import Client, Project, User


class UserSerializer(serializers.ModelSerializer):

    clients = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), many=True)
    projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True)

    class Meta:
        model = User
        fields = ["id", "email", "clients", "projects"]
