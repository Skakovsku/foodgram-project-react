from rest_framework import exceptions

from recipes.models import Product, Recipe, RecipeUsers, Tag

from . import exceptions as exc


def ingredient_validator(data):

    if 'ingredients' not in data:
        raise exceptions.ValidationError(
            {'ingredients': ["Обязательное поле."]}
        )
    if len(data['ingredients']) == 0:
        raise exceptions.ValidationError(
            {'ingredients': "Необходимо заполнить значения поля."}
        )
    list_product = []
    for ingredient in data['ingredients']:
        if 'id' in ingredient:
            if ingredient['id'] in list_product:
                raise exceptions.ValidationError(
                    {'ingredients': "Повтор ингредиентов нецелесообразен."}
                )
            list_product.append(ingredient['id'])
        prod_list = Product.objects.filter(id=ingredient['id'])
        if prod_list.count() == 0:
            raise exc.NotFoundCastom
        if 'id' not in ingredient or type(ingredient['id']) != int:
            raise exceptions.ValidationError(
                {'ingredients': "Некорректное значение поля."}
            )
        if 'amount' not in ingredient:
            raise exceptions.ValidationError(
                {'ingredients': "Некорректное значение поля."}
                )
        msg_amount = "Количество ингредиента: Требуется положительное число."
        if int(ingredient['amount']) < 1:
            raise exceptions.ValidationError(
                {'amount': msg_amount}
            )


def tags_validator(data):
    if 'tags' not in data:
        raise exceptions.ValidationError(
            {'tags': ["Обязательное поле."]}
        )
    if len(data['tags']) == 0:
        raise exceptions.ValidationError(
            {'tags': "Необходимо заполнить значения поля."}
        )
    for tag in data['tags']:
        if type(tag) != int:
            raise exceptions.ValidationError(
                {'tags': "Некорректное значение поля."}
            )
        tags_list = Tag.objects.filter(id=tag)
        if tags_list.count() == 0:
            raise exc.NotFoundCastom


def recipe_users_validator(request, pk):
    if RecipeUsers.objects.filter(user=request.user).count() == 0:
        RecipeUsers.objects.create(user=request.user)
    data_obj = RecipeUsers.objects.get(user=request.user)
    recipe = Recipe.objects.filter(id=pk)
    if recipe.count() == 0:
        raise exc.NotFoundCastom
    return data_obj, recipe[0]
