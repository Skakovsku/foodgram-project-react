from colorful.fields import RGBColorField
from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Tag(models.Model):

    name = models.CharField(max_length=100, verbose_name='tags_name')
    color = RGBColorField(max_length=8, verbose_name='tags_color')
    slug = models.SlugField(max_length=15, verbose_name='tags_slug')


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='ingredients_name')
    measurement_unit = models.CharField(max_length=15, verbose_name='unit')


class Ingredient(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product',
        verbose_name='product',
    )
    amount = models.FloatField(verbose_name='amount')


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='author',
    )
    name = models.CharField(
        max_length=100,
        verbose_name='recipe_name',
    )
    text = models.TextField(verbose_name='description')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(limit_value=1)],
        verbose_name='cooking_time',
    )
    image = models.ImageField(upload_to='recipes/')
    tags = models.ManyToManyField(Tag, verbose_name='recipes_tags')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='ingredient',
    )


class Favourites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users_favoutites',
        verbose_name='favourites',
    )
    recipe = models.ManyToManyField(Recipe, verbose_name='users_recipe')
