from django.urls import path
from .views import ListUserViewSet, ListSubscriptionsViewSet

app_name = 'users'

urlpatterns = [
    path('subscriptions/', ListSubscriptionsViewSet.as_view({'get': 'list'})),
    path('', ListUserViewSet.as_view({'get': 'list',
                                      'post': 'create'})),
]
