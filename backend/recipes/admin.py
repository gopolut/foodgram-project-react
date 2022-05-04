from unittest import mock
from django.contrib import admin

from .models import Recipe

class RecipesAdmin(admin.ModelAdmin):
    '''  '''

    list_diplay = (
        'name',
        'image',
        'text',
        'cooking_time',
    )

admin.site.register(Recipe, RecipesAdmin)
