# Generated by Django 2.2.19 on 2022-06-17 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20220617_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeusers',
            name='users_favorite',
            field=models.ManyToManyField(related_name='favorite', to='recipes.Recipe', verbose_name='users_favorite'),
        ),
        migrations.AlterField(
            model_name='recipeusers',
            name='users_shopping',
            field=models.ManyToManyField(related_name='shopping', to='recipes.Recipe', verbose_name='users_shopping'),
        ),
    ]
