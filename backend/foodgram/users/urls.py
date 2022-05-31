from django.urls import path
from .tokens import EmailObtainAuthToken, token_logout

app_name = 'users'

urlpatterns = [
    path('login/', EmailObtainAuthToken.as_view()),
    path('logout/', token_logout, name='token_logout'),
]
