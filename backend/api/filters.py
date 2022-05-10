from django_filters import rest_framework

from recipes.models import Ingredient, Recipe


class RecipeFilter(rest_framework.FilterSet):
    '''

    '''
    tags = rest_framework.filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        fields = ('author',)
        model = Recipe

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if self.request.query_params.get('is_favorited') in [
            '1', 'true', 'True'
        ]:
            queryset = queryset.filter(recipes_fav__user=self.request.user)
        if self.request.query_params.get('is_in_shopping_cart') in [
            '1', 'true', 'True'
        ]:
            queryset = queryset.filter(recipes_shop__user=self.request.user)
        return queryset


class IngredientFilter(rest_framework.FilterSet):
    '''    '''
    name = rest_framework.filters.CharFilter(field_name='name', lookup_expr='begin')

    class Meta:
        fields = ('name',)
        model = Ingredient
