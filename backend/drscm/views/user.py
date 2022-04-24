from rest_framework.permissions import IsAuthenticated
from drscm.serializers.user import UserSerializer
from drscm.models.user import User
from rest_framework import generics


class ListUsersView(generics.ListAPIView):

    view_name = "list_users_view"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            query_set = User.objects.all()
        else:
            query_set = User.objects.filter(pk=user.id)

        return query_set
