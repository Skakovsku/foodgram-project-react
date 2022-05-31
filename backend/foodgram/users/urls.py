from django.urls import path
from .tokens import EmailObtainAuthToken

app_name = 'users'

urlpatterns = [
    path('login/', EmailObtainAuthToken.as_view()),
]
