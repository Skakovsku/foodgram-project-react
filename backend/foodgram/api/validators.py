from rest_framework import exceptions
from recipes.models import Product, Tag


def ingredient_validator(data):

    if 'ingredients' not in data:
        raise exceptions.ValidationError(
            {'ingredients': ["Обязательное поле."]}
        )
    if len(data['ingredients']) == 0:
        raise exceptions.ValidationError(
            {'ingredients': "Необходимо заполнить значения поля."}
        )
    for ingredient in data['ingredients']:
        prod_list = Product.objects.filter(id=ingredient['id'])
        if prod_list.count() == 0:
            raise exceptions.NotFound(
                {"detail": "Страница не найдена."}
            )
        if 'id' not in ingredient or type(ingredient['id']) != int:
            raise exceptions.ValidationError(
                {'ingredients': "Некорректное значение поля."}
            )
        if 'amount' not in ingredient or type(ingredient['amount']) != int:
            raise exceptions.ValidationError(
                {'ingredients': "Некорректное значение поля."}
                )


def tags_validator(data):
    print(data)
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
            raise exceptions.NotFound(
                {"detail": "Страница не найдена."}
            )