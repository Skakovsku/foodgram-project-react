from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
#router.register('user', UserViewSet)

urlpatterns = [
    path('auth/token/', include('users.urls')),
]
