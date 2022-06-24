from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.tokens import EmailObtainAuthToken, token_logout

from .views import (ProductViewSet, RecipeViewSet, TagViewSet,
                    download_shopping_cart)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', ProductViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('auth/token/login/', EmailObtainAuthToken.as_view()),
    path('auth/token/logout/', token_logout, name='token_logout'),
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path('users/', include('users.urls')),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
]
