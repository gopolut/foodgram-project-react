from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.CharField()
    measurement_unit = serializers.CharField()
    
    class Meta:
        model = User
        fields = (
            'pk',
            'ingredient',
            'measurement_unit',
        )
    

class CustomTokenSerializer(serializers.ModelSerializer):
    # password = serializers.CharField()
    # email = serializers.EmailField()

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
