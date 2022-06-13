from rest_framework import exceptions, viewsets, permissions
from rest_framework.filters import SearchFilter
from recipes.models import Ingredient, Product, Recipe, Tag
from . import serializers, validators


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

    def create(self, request, *args, **kwargs):
        data_valid = self.request.data
        validators.ingredient_validator(data_valid)
        validators.tags_validator(data_valid)
        return super().create(request, *args, **kwargs)

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

    def update(self, request, *args, **kwargs):
        perm_msg_1 = 'У вас недостаточно прав для выполнения '
        perm_msg_2 = 'данного действия.'
        perm_msg = perm_msg_1 + perm_msg_2
        obj = Recipe.objects.filter(id=kwargs['pk'])
        if obj[0].author != self.request.user:
            raise exceptions.PermissionDenied(
                {"detail": perm_msg}
            )
        if obj.count() == 0:
            raise exceptions.NotFound(
                {"detail": "Страница не найдена."}
            )
        if 'ingredients' in self.request.data:
            validators.ingredient_validator(self.request.data)
        if 'tags' in self.request.data:
            validators.tags_validator(self.request.data)
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        return super().perform_update(serializer)
