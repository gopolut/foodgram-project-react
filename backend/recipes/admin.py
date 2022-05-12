from django.contrib import admin

from .models import TAG_CHOICES, Follow, Ingredient, Recipe, Tag


class InlineIngredient(admin.TabularInline):
    model = Recipe.ingredients.through
    verbose_name = 'Ингредиент'


class InlineTag(admin.TabularInline):
    model = Recipe.tags.through
    verbose_name = 'Тег'


class TagFilter(admin.SimpleListFilter):
    title = 'Теги'
    parameter_name = 'теги'

    def lookups(self, request, model_admin):
        return TAG_CHOICES

    def queryset(self, request, queryset):
        if self.value() == 'breakfast':
            return queryset.filter(tags=1)
        elif self.value() == 'lunch':
            return queryset.filter(tags=2)
        elif self.value() == 'dinner':
            return queryset.filter(tags=3)
        elif self.value() == 'supper':
            return queryset.filter(tags=4)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'image',
        'author',
        'cooking_time',
        'favorited_count',
    )
    list_display_links = (
        'pk',
        'name',
    )
    search_fields = (
        'author__username',
        'name',
    )
    list_filter = (
        'author__first_name',
        'name',
        TagFilter,
    )
    sortable_by = (
        'name',
        'author',
        'favorited_count',
    )
    fields = (
        'name',
        'favorited_count',
        'image',
        'author',
        'text',
        'cooking_time',
    )
    readonly_fields = ('favorited_count', )
    autocomplete_fields = ('author', )
    inlines = (InlineIngredient, InlineTag, )
    raw_id_fields = ('author',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_display_links = (
        'pk',
        'name',
    )
    list_filter = (
        'name',
    )
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    list_display_links = (
        'pk',
        'name',
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'user',
        'author',
    )
