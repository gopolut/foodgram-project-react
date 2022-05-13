from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (Favorited, Follow, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag, TagRecipe)

from users.models import CustomUser


class CreateUserSerializer(UserCreateSerializer):
    '''Кастомный сериализатор для регистрации пользователя.'''

    class Meta:
        fields = (
            '__all__'
        )
        read_only_fields = (
            'id',
        )
        model = CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    '''Кастомный сериализатор для вывода данных профиля пользователя.'''

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        # если заменить на __all__, то при GET /api/users/{id}/ появляется
        # много лишних полей не предусмотренных т/з
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        model = CustomUser

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class RecipeIngredientSerializer(serializers.ModelSerializer):
    '''Используется для вывода ингредиентов
    в сериализаторе RecipeReadSerializer.
    '''

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        model = RecipeIngredient


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор для ингредиентов.'''

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        model = Ingredient


class IngredientWriteSerializer(serializers.ModelSerializer):
    '''Сериализатор для сохранения ингредиентов,
    используется в RecipeReadSerializer.
    '''

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'amount',
        )
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор для тегов.'''

    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        model = Tag


class TagRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор для тегов, назначенных рецептам.'''

    name = serializers.ReadOnlyField(source='tag.name')
    color = serializers.ReadOnlyField(source='tag.color')
    slug = serializers.ReadOnlyField(source='tag.slug')

    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        model = TagRecipe


class RecipeReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для вывода рецептов.'''

    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer()

    class Meta:
        fields = (
            '__all__'
        )
        model = Recipe

    def get_tags(self, obj):
        queryset = TagRecipe.objects.filter(recipe=obj)
        return TagRecipeSerializer(queryset, many=True).data

    def get_ingredients(self, obj):
        queryset = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return(
            not request.user.is_anonymous
            and Favorited.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return(
            not request.user.is_anonymous
            and ShoppingCart.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    '''Сериализатор для добавления рецепта в БД.'''

    tags = SlugRelatedField(
        slug_field='id',
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientWriteSerializer(many=True)
    cooking_time = serializers.IntegerField()

    class Meta:
        fields = (
            '__all__'
        )
        model = Recipe

    def calculate_ingredients(self, ingredients, recipe):
        '''Метод для добавления ингрединтов в БД.'''

        for ingredient in ingredients:
            obj = get_object_or_404(Ingredient, id=ingredient['id'])
            amount = ingredient['amount']
            if RecipeIngredient.objects.filter(
                    recipe=recipe,
                    ingredient=obj
            ).exists():
                amount += ingredient['amount']
            RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                ingredient=obj,
                defaults={'amount': amount}
            )

    def validate(self, data):
        '''Проверка на уникальность рецепта
        и наличия обязательных полей.
        '''
        fields = ['tags', 'ingredients', 'name', 'text', 'cooking_time']

        request = self.context.get('request')
        reciipe_name = data.get('name')
        reciipe_text = data.get('text')

        if request.method == 'POST' and Recipe.objects.filter(
            author=request.user,
            name=reciipe_name,
            text=reciipe_text
        ).exists():
            raise serializers.ValidationError({
                f'{reciipe_name}': 'Рецепт с таким название уже существует!'
            })

        for element in fields:
            if element not in data:
                raise ValidationError({
                    f'{element}': 'Поле отсутствует!'
                })
        return data

    def create(self, validated_data):
        '''Метод для создания рецепта,
        добавления ингредиентов и тегов при PATCH-запросе.
        '''

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        self.calculate_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        '''Метод для обновления рецепта при PATCH-запросе.'''

        if 'ingredients' in self.validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.calculate_ingredients(ingredients, instance)

        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def validate_tags(self, data):
        if len(data) == 0:
            raise ValidationError({
                'tags':
                'Добавьте одно или несколько значений в поле tags'
            })
        return data

    def validate_ingredients(self, data):
        for element in data:
            id = element.get('id')
            amount = element.get('amount')

            if not id and id != 0:
                raise ValidationError({
                    'id': 'Это поле обязательно!'
                })
            if not amount and amount != 0:
                raise ValidationError({
                    'amount': 'Это поле обязательно!'
                })

            if id < 1:
                raise ValidationError({
                    'id': 'Значение должно быть >= 1.'
                })
            if amount < 1:
                raise ValidationError({
                    'amount': 'Значение должно быть >= 1.'
                })
        return data

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class ShortRecipeSerializer(serializers.ModelSerializer):
    '''Упрощенный сериализатор, предназначен для вывода рецептов
    в сериализаторах ShoppingCartSerializer и SubscriptionsSerializer
    '''

    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        model = Recipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    '''Сериализатор для добавления/удаления рецептов в список покупок.'''

    class Meta:
        fields = ('__all__')
        model = ShoppingCart

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST' and ShoppingCart.objects.filter(
            user=request.user,
            recipe=data['recipe'].id
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже находится в списке покупок!'
            )
        return data

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')},
        ).data


class FavoritedSerializer(serializers.ModelSerializer):
    '''Сериализатор для добавления/удаления рецептов избранное.'''

    class Meta:
        fields = ('__all__')
        model = Favorited

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST' and Favorited.objects.filter(
            user=request.user,
            recipe=data['recipe'].id
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное!'
            )
        return data

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance.recipe,
            context={'request': self.context.get('request')},
        ).data


class SubscribersReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для вывода данных пользователей,
    используется в FollowSerializer.
    '''

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        # если заменить на __all__-
        # ругается на отсутсвие поля recipes, is_subscribed, is_subscribed
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        model = CustomUser

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return(
            not request.user.is_anonymous
            and Follow.objects.filter(
                user=obj,
                author=request.user,
            ).exists()
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        else:
            recipes = obj.recipes.all()

        return ShortRecipeSerializer(
            recipes,
            many=True,
            read_only=True,
        ).data


class FollowSerializer(serializers.ModelSerializer):
    '''Сериализатор для подписок/отписок на пользователей.'''

    class Meta:
        fields = '__all__'
        model = Follow

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            if request.user == data['author']:
                raise serializers.ValidationError({
                    'errors': 'Невозможно подписаться на самого себя!'
                }
                )

        if Follow.objects.filter(
                user=request.user,
                author=data['author']
        ).exists():
            raise serializers.ValidationError({
                'errors': 'Вы уже подписаны на этого автора!'
            }
            )
        return data

    def to_representation(self, instance):
        return SubscribersReadSerializer(
            instance.author,
            context={'request': self.context.get('request')},
        ).data
