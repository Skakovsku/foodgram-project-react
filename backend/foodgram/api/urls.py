from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.tokens import EmailObtainAuthToken, token_logout
from .views import (ProductViewSet, RecipeViewSet, TagViewSet,
                    download_shopping_cart)

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', ProductViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('auth/token/login/', EmailObtainAuthToken.as_view()),
    path('auth/token/logout/', token_logout, name='token_logout'),
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path('users/', include('users.urls')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
