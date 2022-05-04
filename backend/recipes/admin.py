from tabnanny import verbose
from django.contrib import admin

from .models import Recipe, Ingredient, RecipeIngredient, Tag


class InlineIngredient(admin.TabularInline):
    '''Для регистрации встроенного редактора в первичном редакторе или
    для редактирования дочерней модели на странице родительской модели.
    '''
    model = Recipe.ingredient.through
    verbose_name = 'Ингредиент'


class InlineTag(admin.TabularInline):
    '''для редактирования дочерней модели Tag
    на странице родительской модели Recipe
    '''
    model = Recipe.tag.through
    verbose_name = 'Тег'


class RecipeAdmin(admin.ModelAdmin):
    '''Редактор модели Recipe - класс,
    указывающий параметры представления модели
    в админке
    '''

    # набор выводимых полей
    list_display = (
        'pk',
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

    verbose_name = 'Рецепт'

    # Перечень полей ForeignKey, ManyToMany, кот. отображаются в виде списка с возможностью поиска
    autocomplete_fields = ('author',)

    # задает кортеж со ссылками на классы встроенных редакторов,
    # регистрир. в текущем редакторе
    inlines = (InlineIngredient, InlineTag, )

    raw_id_fields = ('author',)


class IngredientAdmin(admin.ModelAdmin):
    '''Редактор модели Ingredient'''

    list_display = (
        'pk',
        'id',
        'ingredient',
        'measurement_unit',
    )

    search_fields = ('ingredient',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    '''Редактор модели RecipeIngredient'''

    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'quantity',
    )


class TagAdmin(admin.ModelAdmin):
    '''Редактор модели Tag'''

    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
# admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Tag, TagAdmin)
