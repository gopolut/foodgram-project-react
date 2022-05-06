from django.urls import include, path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

# from .views import ingredient_list, ingredient_detail
from . import views


urlpatterns = [
    # path('auth/token/login/', CustomAuthToken.as_view()),
    # path('ingredients/', ingredient_list),
    # path('ingredients/<int:pk>', ingredient_detail),
    url(r'^ingredients/$', views.Ingredientlist.as_view()),
    url(r'^ingredients/(?P<pk>[0-9]+)/$', views.IngredientDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
