from django.db import models

from users.models import CustomUser


COLOR_CHOICES =(
    ('#E26C2D', 'Оранжевый'),
    ('#00ff00', 'Зеленый'),
    ('#3b2fff', 'Синий'),
    ('#540099', 'Фиолетовый')
)

TAG_CHOICES =(
    ('breakfast', 'Завтрак'),
    ('lunch', 'Ланч'),
    ('dinner', 'Обед'),
    ('supper', 'Ужин'),
)

class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'        
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        choices=TAG_CHOICES,
    )
    color = models.CharField(
        max_length=7,
        choices=COLOR_CHOICES,
        verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        unique=True,
        default='-пусто-',
        verbose_name='URL тега'
    )
    
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
        blank=True
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
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    
    def __str__(self):
        return self.name

    def favorited_count(self):
        ''''''
        return self.recipes_fav.count()

    favorited_count.short_description = 'Число добавлений в избранное'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Название рецепта'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
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


class Favorited(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL, # CASCADE
        related_name='user',
        verbose_name='Пользователь(Кто добавил)',
        null=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,  # CASCADE
        related_name='recipes_fav',
        verbose_name='Название рецепта',
        null=True,
    )

    # TODO: добавить models.UniqueConstraint()


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,   # CASCADE
        related_name='buyer',
        verbose_name='Покупатель(Кто добавил)',
        null=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,   # CASCADE
        related_name='recipes_shop',
        verbose_name='Название рецепта',
        null=True,
    )

    # TODO: добавить models.UniqueConstraint()


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='follower',
        verbose_name='Подписчик',
        null=True
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='following',
        verbose_name='Автор канала',
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='uniq_following'
            )
        ]
