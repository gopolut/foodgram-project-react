from django.contrib.auth import get_user_model
from django.forms import ValidationError
from pkg_resources import require
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, Recipe, RecipeIngredient, Favorited, ShoppingCart, Tag, TagRecipe, Follow

from .functions import calculate_ingredients

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        model = User

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False  
        return Follow.objects.filter(user=request.user, author=obj).exists()


class RecipeIngredientSerializer(serializers.ModelSerializer):
    
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
    name = serializers.CharField()
    measurement_unit = serializers.CharField()
    
    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        model = Ingredient
        lookup_field = 'id'


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'amount',
        )


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        model = Tag
        lookup_field = 'id'


class TagRecipeSerializer(serializers.ModelSerializer):
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


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipe


    def get_tags(self, obj):
        queryset = TagRecipe.objects.filter(recipe=obj)
        return TagRecipeSerializer(queryset, many=True).data
    
    def get_ingredients(self, obj):
        # print('context: ', self)
        queryset = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(queryset, many=True).data
    
    def get_is_favorited(self, obj):
        print('context: ', self)
        request = self.context.get('request')
        print('------', request.user)
        if not request or request.user.is_anonymous:
            return False        
        return Favorited.objects.filter(user=request.user, recipe=obj).exists()

    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False        
        return ShoppingCart.objects.filter(user=request.user, recipe=obj).exists()        


class RecipeWriteSerializer(serializers.ModelSerializer):

    tags = SlugRelatedField(
        slug_field='id',
        queryset=Tag.objects.all(),
        many=True
    )
    # ingredients = SlugRelatedField(
    #     slug_field='id',
    #     queryset=Ingredient.objects.all(),
    #     many=True
    # )

    ingredients = IngredientWriteSerializer(many=True)

   
    class Meta:
        fields = (
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipe

    def validate(self, data):
        '''
        Проверка на уникальность рецепта и наличия обязательных полей.
        '''
        fields = ['tags', 'ingredients', 'name', 'text', 'cooking_time']
        print('data--validate--', data)

        request = self.context.get('request')
        reciipe_name = data.get('name')
        reciipe_text = data.get('text')

        print('data--reciipe_name--', reciipe_name)
        
        if request.method == 'POST' and Recipe.objects.filter(
            author=request.user,
            name=reciipe_name,
            text=reciipe_text
        ).exists():
            raise serializers.ValidationError({
                f'{reciipe_name}': 'Рецепт с таким название уже существует!'
            })

        for element in fields:
            # print('element_0000:', element )
            if not element in data:
                raise ValidationError({
                  f'{element}': f'Поле отсутствует!'  
                })
        return data

    def create(self, validated_data):
        '''Метод для создания рецепта и добавления ингредиентов и тегов при PATCH-запросе.
        '''
        print('-----', validated_data)
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
    
        calculate_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        '''Метод для обновления рецепта при PATCH-запросе
        '''

        if 'ingredients' in self.validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            
            calculate_ingredients(ingredients, instance)
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data

    
    def validate_tags(self, data):
        # print('data_id:__', data)
        # print('self.instance:__', self.instance.id)
        
        if len(data) == 0:
             raise ValidationError({
                        'tags':'Добавьте одно или несколько значений в поле tags'
                    }) 

        for tag in data:
            print('tag:', tag.id)
        
        # if self.context['request'].method == 'PATCH':
        #     if Recipe.objects.filter(
        #         id=self.instance.id,
        #         tags=tag.id).exists():
        #             raise ValidationError({
        #                 'tags':f'Тег {tag.id} уже назначен!'
        #             })

        return data
    
    def validate_ingredients(self, data):
        # print('data----', data)      

        for element in data: # OrderedDict([('id', 1), ('amount', 1)])
            
            # print('get_: ', element.get('id'))
            id = element.get('id')
            amount = element.get('amount')
            
            if not id and id != 0:
                raise ValidationError({
                'id':'Это поле обязательно!'
            })
            if not amount and amount!= 0:
                raise ValidationError({
                'amount':'Это поле обязательно!'
            })
            
            if id < 1:
               raise ValidationError({
                'id': 'Значение должно быть >= 1.'
            })
            if amount < 1:
               raise ValidationError({
                'amount': 'Значение должно быть >= 1.'
            })

        # for element in data:    

        # print('____data: ', data[0]['id'])
        # print('____data: ', data[0]['amount'])
        return data


class RecipeSerializerForShoppingCart(serializers.ModelSerializer):
    '''
    
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

    class Meta:
        fields = ('__all__')
        model = ShoppingCart

   
    def to_representation(self, instance):
        return RecipeSerializerForShoppingCart(
            instance.recipe,
            context={'request': self.context.get('request')},
        ).data


    def validate(self, data):
        request = self.context['request']
        if request.method == 'GET' and ShoppingCart.objects.filter(
            user=request.user,
            recipe=data['recipe'].id
        ).exists():
            raise serializers.ValidationError(
                'fffffffffffffffffffffffffff'
            )
        return data

    # def get_cooking_time(self, obj):
    #    print('get_cooking_time_____: ', obj)
    #    recipe_id = self.context['request'].parser_context['kwargs']['id']
    #    print('recipe_id_____: ', recipe_id)
    #    queryset = Recipe.objects.get(pk=recipe_id)
    #    cooking_time = queryset.cooking_time
    #    print('queryset----cooking_time: ', cooking_time)
    #    return cooking_time



class CustomTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

    def validate(self, data):
        print('data: ', data)
        print('password: ', data['password'])
        email = data['email']
        print('email: ', data['email'])
        user = get_object_or_404(User, email=email)
        print('user: ', user)
        # password = self.context["request"].password
        # method = self.context["request"].method
        # print(f'author: {password}, method: {method}')
        return data
    
    def create(self, validated_data):
        print('**validated_data: ', **validated_data)
    
