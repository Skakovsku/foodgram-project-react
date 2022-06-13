from rest_framework import exceptions, viewsets, permissions
from rest_framework.filters import SearchFilter
from recipes.models import Ingredient, Product, Recipe, Tag
from . import serializers


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        obj = Tag.objects.filter(pk=kwargs['pk'])
        if len(obj) == 0:
            raise exceptions.NotFound(
                {'detail': 'Страница не найдена.'}
            )
        return super().retrieve(request, *args, **kwargs)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter,)  # Если db='Postgrees',
    search_fields = ('^name',)         # то нечувствителен к регистру


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        list_ingredients = []
        for ingredient in self.request.data['ingredients']:
            current_ingredient = Ingredient.objects.create(
                product=Product.objects.get(id=ingredient['id']),
                amount=ingredient['amount']
            )
            list_ingredients.append(current_ingredient)
        serializer.save(
            author=self.request.user,
            tags=self.request.data['tags'],
            ingredients=list_ingredients
        )
