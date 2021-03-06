from django.contrib import admin

from recipes.models import Ingredient, Product, Recipe, Tag
from users.models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username',)


@admin.register(Subscription, Tag, Product)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount',)
    list_filter = ('product',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_count',)
    list_filter = ('author', 'name', 'tags',)

    def favorite_count(self, obj):
        favorite_count = obj.favorite.all().count()
        return f'Добавлено в ИЗБРАННОЕ {favorite_count} раз'
