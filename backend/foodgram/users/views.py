from djoser.views import UserViewSet
from rest_framework import exceptions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
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
    lookup_url_kwarg = 'subscription_id'

    def perform_create(self, serializer):
        follow_list = User.objects.filter(pk=self.kwargs['subscription_id'])
        if len(follow_list) == 0:
            raise exceptions.NotFound(
                {'detail': 'Страница не найдена.'}
            )
        subscription = User.objects.get(pk=self.kwargs['subscription_id'])
        user = self.request.user
        if subscription == user:
            raise exceptions.ValidationError(
                detail={'errors': 'Нельзя подписаться на себя.'}
            )
        valid_subscription = Subscription.objects.filter(
            user=user,
            following=subscription
        )
        if len(valid_subscription) != 0:
            raise exceptions.ValidationError(
                detail={
                    'errors': 'Нельзя подписаться дважды на одного автора.'
                }
            )
        serializer.save(
            user=user,
            following=subscription
        )

    def destroy(self, request, *args, **kwargs):
        follow_list = User.objects.filter(pk=self.kwargs['subscription_id'])
        if len(follow_list) == 0:
            raise exceptions.NotFound(
                {'detail': 'Страница не найдена.'}
            )
        subscription_list = Subscription.objects.filter(
            user=request.user,
            following=follow_list[0]
        )
        if len(subscription_list) == 0:
            raise exceptions.ValidationError(
                detail={
                    'errors': 'У вас нет подписки на этого автора.'
                }
            )
        obj = Subscription.objects.get(
            user=request.user,
            following=follow_list[0]
        )
        self.perform_destroy(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)
