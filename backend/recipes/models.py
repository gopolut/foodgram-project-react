from django.db import models

from users.models import User


class Ingredient(models.Model):
    ingredient = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'        
    )

    def __str__(self):
        return self.ingredient


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        null=True,
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Опишите процесс приготовления блюда'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Название рецепта'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Название ингредиента'
    )
    quantity = models.IntegerField(
        verbose_name='Количество',
    )

    # def __str__(self):
    #     return ''
