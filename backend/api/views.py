from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from django.http import Http404

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets

from recipes.models import Ingredient, Recipe
from .serializers import CustomTokenSerializer, IngredientSerializer, RecipeSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


# @csrf_exempt
# @api_view(['GET', 'POST'])
class Ingredientlist(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
# def ingredient_list(request, format=None):
# if request.method == 'GET':
    lookup_field = 'slug'
    def get(self, request, format=None):
        ingredient = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredient, many=True)
        return Response(serializer.data)
    
    # elif request.method == 'POST':
    def post(self, request, format=None):
        # data = JSONParser().parse(request)
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def ingredient_detail(request, pk, format=None):
class IngredientDetail(APIView):
    """Retrieve ingredient."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_field = 'slug'
   
    def get_object(self, pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            # return Response(status=status.HTTP_404_NOT_FOUND)
            raise Http404
    
    # if request.method == 'GET':
    def get(self, request, pk, format=None):
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)


# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer


class RecipeList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    
    def get(self, request):
        recipe = Recipe.objects.all()
        # добавил request в словаре контекст, т.к. сериализатор не получал реквест
        # и не было возможности получить имя польз. (request.user) 
        serializer = RecipeSerializer(recipe, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise Http404
    
    # if request.method == 'GET':
    def get(self, request, pk, format=None):
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(serializer.data)
