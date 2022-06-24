from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Subscription, User


class EmailAuthTokenSerializer(serializers.Serializer):

    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.get(email=email)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password',)


class CurrentUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed',)

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False
        follow = Subscription.objects.filter(
            user=current_user,
            following=obj
        )
        if len(follow) == 0:
            return False
        return True


class ListSubscriptionsSerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'recipes', 'recipes_count',)

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class PostDelSubscribeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id']
