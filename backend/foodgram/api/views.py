from curses.ascii import HT
from rest_framework import exceptions, viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django.http import HttpResponse
from recipes.models import Ingredient, Product, Recipe, RecipeUsers, Tag
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
            product = Product.objects.get(id=ingredient['id'])
            ingredient_request = Ingredient.objects.filter(
                product=product,
                amount=ingredient['amount']
            )
            if ingredient_request.count() != 0:
                current_ingredient = ingredient_request['0']
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
            raise exceptions.NotFound(
                {"detail": "Страница не найдена."}
            )
        if obj[0].author != self.request.user:
            raise exceptions.PermissionDenied(
                {"detail": perm_msg}
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(methods=['post', 'delete'], detail=True,
            url_path='shopping_cart', url_name='change_password')
    def shopping_cart(self, request, pk):
        print(request.method)
        print(self, request, pk)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        print(request.method)
        print(self, request, pk)


@action(methods=['get'], detail=True, url_path='download_shopping_cart')
def download_shopping_cart(request):
    print(request)
    return HttpResponse()
