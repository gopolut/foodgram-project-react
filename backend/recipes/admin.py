from django.contrib import admin

from .models import Recipe, Ingredient, RecipeIngredient

class RecipesAdmin(admin.ModelAdmin):
    '''  '''

    list_diplay = (
        'id',
        'name',
        'image',
        'text',
        'cooking_time',
    )


class IngredientAdmin(admin.ModelAdmin):
    '''  '''

    list_diplay = (
        'id',
        'ingredient',
        'measurement_unit',
    )


class RecipeIngredientAdmin(admin.ModelAdmin):
    '''  '''

    list_diplay = (
        'id',
        'recipe',
        'ingredient',
        'quantity',
    )


admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
