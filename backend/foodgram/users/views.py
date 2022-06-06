from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from users.models import User, Subscription
from .serializers import (PostDelSubscribeSerialiser,
                          ListSubscriptionsSerializer)


class ListUserViewSet(UserViewSet):

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class ListSubscriptionsViewSet(ModelViewSet):
    serializer_class = ListSubscriptionsSerializer

    def get_queryset(self):
        follower = Subscription.objects.filter(user=self.request.user)
        users = []
        for user in follower:
            users.append(user.following)
        new_queryset = users
        return new_queryset


class PostDelSubscribeViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = PostDelSubscribeSerialiser

    def perform_create(self, serializer):
        subscription = User.objects.get(
            pk=self.kwargs['subscription_id']
        )
        serializer.save(
            user=self.request.user,
            following=subscription
        )
