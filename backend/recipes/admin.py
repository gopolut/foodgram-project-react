from django.contrib import admin

from .models import Recipe, Ingredient, RecipeIngredient


class InlineIngredient(admin.TabularInline):
    '''Для регистрации встроенного редактора в первичном редакторе или
    для редактирования родительской модели на странице родительской модели.
    '''
    model = Recipe.ingredient.through
    verbose_name = 'Ингредиент'

class RecipeAdmin(admin.ModelAdmin):
    '''Редактор модели Recipe - класс,
    указывающий параметры представления модели
    в админке
    '''

    # набор выводимых полей
    list_diplay = (
        'name',
        'image',
        'author',
        'text',
        'cooking_time',
    )

    # последовательность выводимых полей
    fields = (
        'name',
        'image',
        'author',
        'text',
        'cooking_time',
    )

    # возвращает поля, которые доступны только для чтения
    # def get_readonly_fields(self, request, obj=None):
    #     f = ['image']
    #     return

    # def get_inlines(self, request, obj=None):
    #     if obj:
    #         return ()
    #     else:
    #         return InlineIngredient


    # Перечень полей ForeignKey, ManyToMany, кот. отображаются в виде списка с возможностью поиска
    autocomplete_fields = ('author',)

    # задает кортеж со ссылками на классы встроенных редакторов,
    # регистрир. в текущем редакторе
    inlines = (InlineIngredient, )

    raw_id_fields = ('author',)


class IngredientAdmin(admin.ModelAdmin):
    '''Редактор модели Ingredient'''

    list_diplay = (
        'id',
        'ingredient',
        'measurement_unit',
    )

    search_fields = ('ingredient',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    '''Редактор модели RecipeIngredient'''

    list_diplay = (
        'id',
        'recipe',
        'ingredient',
        'quantity',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
