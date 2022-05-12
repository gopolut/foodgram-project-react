from django.urls import include, path
from rest_framework.routers import DefaultRouter

from djoser.views import TokenDestroyView

from . import views

app_name = 'api'

router = DefaultRouter()

router.register(
    r'users',
    views.CustomUserViewSet,
    basename='users'
)
router.register(
    r'tags',
    views.TagViewSet,
    basename='tags'
)
router.register(
    r'recipes',
    views.RecipeViewSet,
    basename='recipes'
)
router.register(
    r'ingredients',
    views.IngredientViewSet,
    basename='ingredients'
)


urlpatterns = [
    path(
        r'recipes/download_shopping_cart/',
        views.DownloadShoppingCartView.as_view(),
        name='shopping_cart'
    ),
    path(
        r'recipes/<int:id>/shopping_cart/',
        views.ShoppingCartView.as_view(),
        name='shopping_cart'
    ),
    path(
        r'recipes/<int:id>/favorite/',
        views.FavoritedView.as_view(),
        name='favorited'
    ),
    path(
        r'users/<int:id>/subscribe/',
        views.FollowingView.as_view(),
        name='following'
    ),
    path(
        r'auth/token/login/',
        views.CustomTokenCreateView.as_view(),
        name='login'
    ),
    path(
        r'auth/token/logout/',
        TokenDestroyView.as_view(),
        name='logout'
    ),
    path(
        r'users/subscriptions/',
        views.SubscriptionsViewSet.as_view({'get': 'list'}),
        name='subscriptions'
     ),
    path('', include(router.urls)),

]
