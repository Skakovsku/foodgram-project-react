# Generated by Django 2.2.19 on 2022-06-15 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_shoppingcart'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_favoutites', to=settings.AUTH_USER_MODEL, verbose_name='favourites')),
                ('users_favorite', models.ManyToManyField(related_name='favorite', to='recipes.Recipe', verbose_name='users_favorite')),
                ('users_shopping', models.ManyToManyField(related_name='shopping', to='recipes.Recipe', verbose_name='users_shopping')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='user',
        ),
        migrations.DeleteModel(
            name='Favourites',
        ),
        migrations.DeleteModel(
            name='ShoppingCart',
        ),
    ]
