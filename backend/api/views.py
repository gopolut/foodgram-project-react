from django import views
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from requests import delete

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from rest_framework.response import Response
from django.http import Http404

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import permissions

from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework import viewsets, views

from recipes.models import Ingredient, Recipe, Tag, ShoppingCart
from .serializers import CustomTokenSerializer, IngredientSerializer, RecipeSerializer, RecipeWriteSerializer, TagSerializer, ShoppingCartSerializer
from .permissions import IsAuthorOrReadOnly
from .viewsets import FavoritedShoppingCartViewSet

User = get_user_model()


# @csrf_exempt
# @api_view(['GET', 'POST'])
# class Ingredientlist(APIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
# # def ingredient_list(request, format=None):
# # if request.method == 'GET':
#     lookup_field = 'slug'
#     def get(self, request, format=None):
#         ingredient = Ingredient.objects.all()
#         serializer = IngredientSerializer(ingredient, many=True)
#         return Response(serializer.data)
    
#     # elif request.method == 'POST':
#     def post(self, request, format=None):
#         # data = JSONParser().parse(request)
#         serializer = IngredientSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def ingredient_detail(request, pk, format=None):
# class IngredientDetail(APIView):
#     """Retrieve ingredient."""
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
#     lookup_field = 'slug'
   
#     def get_object(self, pk):
#         try:
#             return Ingredient.objects.get(pk=pk)
#         except Ingredient.DoesNotExist:
#             # return Response(status=status.HTTP_404_NOT_FOUND)
#             raise Http404
    
#     # if request.method == 'GET':
#     def get(self, request, pk, format=None):
#         ingredient = self.get_object(pk)
#         serializer = IngredientSerializer(ingredient)
#         return Response(serializer.data)


class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeWriteSerializer


class ShoppingCartView(views.APIView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    # serializer_class = ShoppingCartSerializer

    # def get_queryset(self):
    #     new_queryset = self.request.user.buyer.all()
    #     return new_queryset

    # def perform_create(self, serializer):
    #     recipe = get_object_or_404(Recipe, pk=self.kwargs.get('id'))
    #     serializer.save(user=self.request.user, recipe=recipe)
    
    
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)


    def create(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        context = {'request': request}
        serializer = ShoppingCartSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)  
        serializer.save()      
        return Response(
        serializer.data,
        status.HTTP_201_CREATED
    )

    def delete(self, request, id):
        # self.perform_destroy(instance)
        # instance = self.get_object(id)
        # instance.delete()

        user=request.user.id
        # recipe_id = self.kwargs.get('id')
        shop = ShoppingCart.objects.get(recipe=id, user=user)
        # shop = get_object_or_404(ShoppingCart, recipe=self.kwargs.get('id'), user=user)
        data = {
            'user': request.user.id,
            'recipe': id
        }
        context = {'request': request}
        serializer = ShoppingCartSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)        
        shop.delete()
        return Response(
        status=status.HTTP_204_NO_CONTENT
        )
    

# class RecipeList(views.APIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    
#     def get(self, request):
#         recipe = Recipe.objects.all()
#         # добавил request в словаре контекст, т.к. сериализатор не получал реквест
#         # и не было возможности получить имя польз. (request.user) 
#         serializer = RecipeSerializer(recipe, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = RecipeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RecipeDetail(APIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
#     def get_object(self, pk):
#         try:
#             return Recipe.objects.get(pk=pk)
#         except Ingredient.DoesNotExist:
#             raise Http404
    
#     # if request.method == 'GET':
#     def get(self, request, pk, format=None):
#         recipe = self.get_object(pk)
#         serializer = RecipeSerializer(recipe, context={'request': request})
#         return Response(serializer.data)
