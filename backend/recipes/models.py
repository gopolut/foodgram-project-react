from django.db import models

from users.models import User


COLOR_CHOICES =(
    ('#E26C2D', 'Оранжевый'),
    ('#00ff00', 'Зеленый'),
    ('#3b2fff', 'Синий'),
)


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


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=7,
        choices=COLOR_CHOICES,
        verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        unique=True, default='-пусто-',
        verbose_name='URL тега'
    )
    
    def __str__(self):
        return self.name


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
    tag = models.ManyToManyField(
        Tag,
        through='TagRecipe'
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


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Название тега'
    )
    recipe = models.ForeignKey(
       Recipe,
       on_delete=models.CASCADE,
       related_name='tags',
       verbose_name='Название рецепта'
    )
