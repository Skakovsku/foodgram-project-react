from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from recipes.models import Ingredient, Product, Recipe, RecipeUsers, Tag

from . import exceptions as exc
from . import filters
from . import get_list_shopping_cart as list_shopping
from . import serializers, validators


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        obj = Tag.objects.filter(pk=kwargs['pk'])
        if len(obj) == 0:
            raise exc.NotFoundCastom
        return super().retrieve(request, *args, **kwargs)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.RecipeFilter

    def create(self, request, *args, **kwargs):
        data_valid = self.request.data
        validators.ingredient_validator(data_valid)
        validators.tags_validator(data_valid)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        list_ingredients = []
        for ingredient in self.request.data['ingredients']:
            product = Product.objects.get(id=ingredient['id'])
            ingredient_request = Ingredient.objects.filter(
                product=product,
                amount=ingredient['amount']
            )
            if ingredient_request.count() != 0:
                current_ingredient = ingredient_request[0]
            else:
                current_ingredient = Ingredient.objects.create(
                    product=product,
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
        if 'ingredients' in self.request.data:
            list_ingredients = []
            for ingredient in self.request.data['ingredients']:
                new_obj = Ingredient.objects.filter(
                    product=Product.objects.get(id=ingredient['id']),
                    amount=ingredient['amount']
                )
                if new_obj.count() != 0:
                    new_ingredient = new_obj[0]
                else:
                    new_ingredient = Ingredient.objects.create(
                        product=Product.objects.get(id=ingredient['id']),
                        amount=ingredient['amount']
                    )
                list_ingredients.append(new_ingredient)
            serializer.save(ingredients=list_ingredients)
        if 'tags' in self.request.data:
            list_tags = []
            for tag in self.request.data['tags']:
                new_obj = Tag.objects.get(id=tag)
                list_tags.append(new_obj)
            serializer.save(tags=list_tags)

    def destroy(self, request, *args, **kwargs):
        perm_msg_1 = 'У вас недостаточно прав для выполнения '
        perm_msg_2 = 'данного действия.'
        perm_msg = perm_msg_1 + perm_msg_2
        obj = Recipe.objects.filter(id=kwargs['pk'])
        if obj.count() == 0:
            raise exc.NotFoundCastom
        if obj[0].author != self.request.user:
            raise exceptions.PermissionDenied(
                {"detail": perm_msg}
            )
        return super().destroy(request, *args, **kwargs)

    @action(methods=['post', 'delete'], detail=True,
            url_path='shopping_cart')
    def shopping_cart(self, request, pk):
        data_obj, recipe = validators.recipe_users_validator(request, pk)
        if request.method == 'DELETE':
            if data_obj.users_shopping.filter(id=pk).count() == 0:
                raise exceptions.ValidationError(
                    {"error": "Запрошенного рецепта нет в списке."}
                )
            data_obj.users_shopping.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST':
            if data_obj.users_shopping.filter(id=pk).count() != 0:
                raise exceptions.ValidationError(
                    {"error": "Запрошенный рецепт уже есть в списке."}
                )
            data_obj.users_shopping.add(recipe)
            obj = data_obj.users_shopping.get(id=pk)
            data = get_data_recipeusers(request, obj)
            return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        data_obj, recipe = validators.recipe_users_validator(request, pk)
        if request.method == 'DELETE':
            if data_obj.users_favorite.filter(id=pk).count() == 0:
                raise exceptions.ValidationError(
                    {"error": "Запрошенного рецепта нет в списке."}
                )
            data_obj.users_favorite.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST':
            if data_obj.users_favorite.filter(id=pk).count() != 0:
                raise exceptions.ValidationError(
                    {"error": "Запрошенный рецепт уже есть в списке."}
                )
            data_obj.users_favorite.add(recipe)
            obj = data_obj.users_favorite.get(id=pk)
            data = get_data_recipeusers(request, obj)
            return Response(data, status=status.HTTP_201_CREATED)


def get_data_recipeusers(request, obj):
    obj_id, obj_name = obj.id, obj.name
    obj_cooking_time = obj.cooking_time
    obj_image_1 = request.META['wsgi.url_scheme'] + '://'
    obj_image_2 = request.META['HTTP_HOST'] + obj.image.url
    obj_image = obj_image_1 + obj_image_2
    data = {
        'id': obj_id,
        'name': obj_name,
        'image': obj_image,
        'cooking_time': obj_cooking_time
    }
    return data


@api_view()
def download_shopping_cart(request):
    if RecipeUsers.objects.filter(user=request.user).count() == 0:
        RecipeUsers.objects.create(user=request.user)
    data_obj = RecipeUsers.objects.get(user=request.user)
    shopping_list_recipes = data_obj.users_shopping.all()
    shopping_list = {}
    for recipe in shopping_list_recipes:
        for ingredient in recipe.ingredients.all():
            if ingredient.product.name not in shopping_list:
                shopping_list[ingredient.product.name] = [
                    ingredient.amount,
                    ingredient.product.measurement_unit
                ]
            else:
                shopping_list[ingredient.product.name][0] += ingredient.amount
    response = list_shopping.get_list_shopping_cart(request, shopping_list)
    return response
