from django.db import models

from colorfield.fields import ColorField

from users.models import CustomUser

# TAGS = (
#     ('Завтрак', 'breakfast', '#E26C2D'),
#     ('Ланч', 'lunch', '#00ff00'),
#     ('Обед', 'dinner', '#3b2fff'),
#     ('Ужин', 'supper', '#8100EA'),
# )


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        # choices=TAG_CHOICES,
    )
    color = ColorField(
        verbose_name='Цветовой HEX-код',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        default='-пусто-',
        verbose_name='URL тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
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
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Опишите процесс приготовления блюда'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания рецепта",
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name

    def favorited_count(self):
        '''Для вывода в админке количества добавленных рецептов в избранное'''

        return self.recipes_fav.count()

    favorited_count.short_description = 'Число добавлений в избранное'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Название рецепта'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Название ингредиента'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
    )


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_recipe',
        verbose_name='Название тега'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tag',
        verbose_name='Название рецепта'
    )

    def __str__(self):
        return (f'{self.tag}: {self.recipe}')


class Favorited(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь(Кто добавил)',
        null=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_fav',
        verbose_name='Название рецепта',
        null=True,
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorited'
            ),
        ]

    def __str__(self):
        return (f'{self.user}: {self.recipe}')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='buyer',
        verbose_name='Покупатель(Кто добавил)',
        null=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes_shop',
        verbose_name='Название рецепта',
        null=True,
    )

    class Meta:
        verbose_name = 'Корзина с покупками'
        verbose_name_plural = 'Корзина с покупками'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping'
            ),
        ]

    def __str__(self):
        return (f'{self.user}: {self.recipe}')


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        null=True
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор канала',
        null=True
    )

    class Meta:
        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчики'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='uniq_following'
            )
        ]

    def __str__(self):
        return (f'{self.user} подписан на: {self.author}')
