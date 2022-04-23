from rest_framework import serializers
from drscm.models import User, Client, Project


class UserSerializer(serializers.ModelSerializer):

    clients = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), many=True)
    projects = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name',
                  'role', 'is_active', 'clients', 'projects']
