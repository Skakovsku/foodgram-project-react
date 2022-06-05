from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from users.models import User, Subscription


class ListUserViewSet(UserViewSet):

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class ListSubscriptionsViewSet(ModelViewSet):
    serializer_class = serializers.ModelSerializer

    def get_queryset(self):
        new_queryset = Subscription.objects.filter(user=self.request.user)
        return new_queryset
