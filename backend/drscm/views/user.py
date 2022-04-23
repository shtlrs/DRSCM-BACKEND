from rest_framework.permissions import IsAuthenticated

from drscm.models import User
from drscm.serializers.user import UserSerializer
from rest_framework import generics


class ListUsersView(generics.ListAPIView):

    view_name = "list_users_view"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

