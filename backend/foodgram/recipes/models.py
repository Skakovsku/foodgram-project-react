from colorful.fields import RGBColorField
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):

    name = models.CharField('tags_name', max_length=100)
    color = RGBColorField('tags_color', max_length=8)
    slug = models.SlugField('tags_slug')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.slug


class Product(models.Model):
    name = models.CharField('ingredients_name', max_length=100)
    measurement_unit = models.CharField('unit', max_length=15)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product',
        verbose_name='product',
    )
    amount = models.IntegerField(verbose_name='amount')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'{self.product}, {self.amount}{self.product.measurement_unit}'


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='author',
    )
    name = models.CharField('recipe_name', max_length=100)
    text = models.TextField(verbose_name='description')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(limit_value=1)],
        default=0,
        verbose_name='cooking_time',
    )
    image = models.ImageField(upload_to='recipes/')
    tags = models.ManyToManyField(Tag, verbose_name='recipes_tags')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='ingredient',
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class RecipeUsers(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='users_favoutites',
        verbose_name='favourites',
    )
    users_favorite = models.ManyToManyField(
        Recipe,
        related_name='favorite',
        verbose_name='users_favorite'
    )
    users_shopping = models.ManyToManyField(
        Recipe,
        related_name='shopping',
        verbose_name='users_shopping'
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.user.username
