from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import ListUserViewSet

app_name = 'api'

router = DefaultRouter()
# router.register('user', UserViewSet)

urlpatterns = [
    path('auth/token/', include('users.urls')),
    path('users/', ListUserViewSet.as_view({'get': 'list',
                                            'post': 'create'})),
    path('', include('djoser.urls')),
]
