from django.urls import include, path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

# При использованиии view-функций и view-классов
# urlpatterns = [
#     # path('auth/token/login/', CustomAuthToken.as_view()),
#     # path('ingredients/', ingredient_list),
#     # path('ingredients/<int:pk>', ingredient_detail),
#     url(r'^ingredients/$', views.Ingredientlist.as_view()),
#     url(r'^ingredients/(?P<pk>[0-9]+)/$', views.IngredientDetail.as_view()),
#     url(r'^recipes/$', views.RecipeList.as_view()),
#     url(r'^recipes/(?P<pk>[0-9]+)/$', views.RecipeDetail.as_view()),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)

# При использованиии ViewSet

router = DefaultRouter()

router.register(r'recipes', views.RecipeViewSet, basename='recipes')
router.register(r'ingredients', views.IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),

]