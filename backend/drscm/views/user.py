from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated
from drscm.serializers.user import UserSerializer
from drscm.models.user import User
from rest_framework import generics


@extend_schema_view(
     get=extend_schema(description='Returns the list of the available users',
                       operation_id="List users"),
 )
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
