from django.urls import include, path
from rest_framework.routers import DefaultRouter

from djoser.views import TokenDestroyView, UserViewSet

from . import views

app_name = 'api'

router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)
router.register(
    'tags',
    views.TagViewSet,
    basename='tags'
)
router.register(
    'recipes',
    views.RecipeViewSet,
    basename='recipes'
)
router.register(
    'ingredients',
    views.IngredientViewSet,
    basename='ingredients'
)


urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        views.DownloadShoppingCartView.as_view(),
        name='shopping_cart'
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        views.ShoppingCartView.as_view(),
        name='shopping_cart'
    ),
    path(
        'recipes/<int:id>/favorite/',
        views.FavoritedView.as_view(),
        name='favorited'
    ),
    path(
        'users/<int:id>/subscribe/',
        views.FollowingView.as_view(),
        name='following'
    ),
    path(
        'auth/token/login/',
        views.CustomTokenCreateView.as_view(),
        name='login'
    ),
    path(
        'auth/token/logout/',
        TokenDestroyView.as_view(),
        name='logout'
    ),
    path(
        'users/subscriptions/',
        views.SubscriptionsViewSet.as_view({'get': 'list'}),
        name='subscriptions'
    ),
    path('', include(router.urls)),
]
