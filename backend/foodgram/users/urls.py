from django.urls import path

from .views import (ListSubscriptionsViewSet, ListUserViewSet,
                    PostDelSubscribeViewSet)

app_name = 'users'

urlpatterns = [
    path('subscriptions/', ListSubscriptionsViewSet.as_view({'get': 'list'})),
    path(
        '<int:subscription_id>/subscribe/',
        PostDelSubscribeViewSet.as_view({'post': 'create',
                                         'delete': 'destroy'})
    ),
    path('', ListUserViewSet.as_view({'get': 'list',
                                      'post': 'create'})),
]
