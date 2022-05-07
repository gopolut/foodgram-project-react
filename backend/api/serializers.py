from django.contrib.auth import get_user_model
from pkg_resources import require
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.relations import SlugRelatedField
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, Recipe, RecipeIngredient, Favorited, ShoppingCart, Tag, TagRecipe, Follow

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
    name = serializers.ReadOnlyField(source='ingredient.ingredient')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'

    )
    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
            'quantity',
        )
        model = RecipeIngredient


class IngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.CharField()
    measurement_unit = serializers.CharField()
    
    class Meta:
        fields = (
            'pk',
            'ingredient',
            'measurement_unit',
        )
        model = Ingredient
        lookup_field = 'slug'



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
