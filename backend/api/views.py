from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import action

from rest_framework.response import Response

from rest_framework import permissions

from django_filters.rest_framework.backends import DjangoFilterBackend
from django.contrib.auth import update_session_auth_hash

from rest_framework.views import APIView
from rest_framework import viewsets

from recipes.models import Ingredient, Recipe, Tag, ShoppingCart, Favorited, Follow
from .serializers import (SubscribersReadSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          TagSerializer, ShoppingCartSerializer,
                          FavoritedSerializer, FollowSerializer,)

from .permissions import IsAuthorOrReadOnly
from .paginations import CustomPaginator
from .filters import IngredientFilter, RecipeFilter

from djoser.views import UserViewSet, TokenCreateView
from djoser import utils
from djoser.compat import get_user_email
from djoser.conf import settings as djoser_settings


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    )
    http_method_names = ['get', 'post']

    @action(['post'], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.validated_data["new_password"])
        self.request.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": self.request.user}
            to = [get_user_email(self.request.user)]
            settings.EMAIL.password_changed_confirmation(
                self.request, context).send(to)

        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            utils.logout_user(self.request)
        elif settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenCreateView(TokenCreateView):
    '''Вьюсет для получения статуса 201'''

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = djoser_settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED
        )


class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    filterset_class = IngredientFilter
    filter_backends = (DjangoFilterBackend,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = CustomPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer


class ShoppingCartView(APIView):   
    def post(self, request, id):
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
        try:    
            
            shop = ShoppingCart.objects.get(recipe=id, user=request.user)
            # shop = get_object_or_404(ShoppingCart, recipe=id, user=request.user)
        except ShoppingCart.DoesNotExist:
            return Response({
                'errors': 'Удаление невозможно, такого рецепта нет в корзине!'
            }, status=status.HTTP_400_BAD_REQUEST   
            )     
        shop.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class FavoritedView(APIView):
        
    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        context = {'request': request}
        serializer = FavoritedSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True) 
        serializer.save()      
        return Response(
            serializer.data,
            status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        try:
            favorited = Favorited.objects.get(recipe=id, user=request.user)
        except Favorited.DoesNotExist:
            return Response({
                'errors' : 'Удаление невозможно, такого рецепта нет в избранном!'
                }, status=status.HTTP_400_BAD_REQUEST
            )    
        favorited.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class DownloadShoppingCartView(APIView):
    
    def get(self, request):
        user = request.user

        shopping_list = user.buyer.values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
            ).annotate(
                sum=Sum('recipe__recipe_ingredient__amount')
                )

        print_list = []
        for element in shopping_list:           
            ingredient = element.get('recipe__ingredients__name')
            unit = element.get('recipe__ingredients__measurement_unit')
            sum = element.get('sum')
            total_ingredient = f'{ingredient}, {unit}: {sum}\n'
            
            print_list.append(total_ingredient)
            
        response = HttpResponse(print_list, 'Content-Type: text/html; charset=utf-8')
        # response = HttpResponse(print_list, content_type=text)
        response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
        return response


class FollowingView(APIView):

    def get_queryset(self):
        return Follow.objects.all()

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'author': id
        }
        context = {'request': request}
        serializer = FollowSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True) 
        serializer.save()      
        return Response(
            serializer.data,
            status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        try:
            follow = Follow.objects.get(author=id, user=request.user)
        except Follow.DoesNotExist:
            return Response({
                'errors' : 'Удаление невозможно, такого автора нет в подписках!'
                }, status=status.HTTP_400_BAD_REQUEST
            )    
        follow.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class SubscriptionsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = CustomPaginator
    serializer_class = SubscribersReadSerializer
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        new_queryset = User.objects.filter(following__user=user)
        return new_queryset
