from io import BytesIO

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http.response import HttpResponse
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from djoser import utils
from djoser.conf import settings as djoser_settings
from djoser.views import TokenCreateView
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .filters import IngredientFilter, RecipeFilter
from .paginations import CustomPaginator
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoritedSerializer, FollowSerializer,
                          IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, ShoppingCartSerializer,
                          SubscribersReadSerializer, TagSerializer)
from backend.settings import FONT_PATH
from recipes.models import (Favorited, Follow, Ingredient, Recipe,
                            ShoppingCart, Tag)

User = get_user_model()


class CustomTokenCreateView(TokenCreateView):

    # Для получения статуса 201
    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = djoser_settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED
        )


class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    )
    filterset_class = IngredientFilter
    filter_backends = (DjangoFilterBackend,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    )
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
                'errors':
                'Удаление невозможно, такого рецепта нет в избранном!'
            }, status=status.HTTP_400_BAD_REQUEST
            )
        favorited.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class DownloadShoppingCartView(APIView):

    def get(self, request, path=FONT_PATH):
        shopping_list = request.user.buyer.values(
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
            total_ingredient = f'{ingredient}, {unit}: {sum}'

            print_list.append(total_ingredient)

        response = HttpResponse(content_type='application/pdf')
        content_disposition = 'attachment; filename="shopping_list.pdf"'
        response['Content-Disposition'] = content_disposition

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, A4)

        pdfmetrics.registerFont(TTFont('FreeSans', path))
        pdf.setFont('FreeSans', 12)

        string_height = 750

        pdf.drawString(50, 800, 'Список ингредиентов')
        pdf.drawString(400, 800, f'Пользователь: {request.user.username}')
        pdf.line(0, 790, 800, 790)

        for line in print_list:
            pdf.drawString(50, string_height, line)
            string_height -= 30

        pdf.showPage()
        pdf.save()

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

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
                'errors': 'Удаление невозможно, такого автора нет в подписках!'
            }, status=status.HTTP_400_BAD_REQUEST
            )
        follow.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class SubscriptionsViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    )
    pagination_class = CustomPaginator
    serializer_class = SubscribersReadSerializer
    http_method_names = ['get']

    def get_queryset(self):
        new_queryset = User.objects.filter(
            following__user=self.request.user
        )
        return new_queryset
