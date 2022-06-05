from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.tokens import EmailObtainAuthToken, token_logout

app_name = 'api'

router = DefaultRouter()
# router.register('user', UserViewSet)

urlpatterns = [
    path('auth/token/login/', EmailObtainAuthToken.as_view()),
    path('auth/token/logout/', token_logout, name='token_logout'),
    path('users/', include('users.urls')),
    path('', include('djoser.urls')),
]
