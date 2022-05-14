from django.db.models import F
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, Recipe, RecipeIngredient


def calculate_ingredients(ingredients, recipe):
    '''
    Метод добавляет ингрединты в БД
    '''

    for ingredient in ingredients:
        obj = get_object_or_404(Ingredient, id=ingredient['id'])
        amount = ingredient['amount']
        if RecipeIngredient.objects.filter(
                recipe=recipe,
                ingredient=obj
        ).exists():
            # amount += F('amount')
            amount += ingredient['amount']
        RecipeIngredient.objects.update_or_create(
            recipe=recipe,
            ingredient=obj,
            defaults={'amount': amount}
        )
