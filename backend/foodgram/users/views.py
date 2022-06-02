from djoser.views import UserViewSet
from users.models import User


class ListUserViewSet(UserViewSet):

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
