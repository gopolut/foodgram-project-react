import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


TAGS = (
    ('Завтрак', 'breakfast', '#E26C2D'),
    ('Ланч', 'lunch', '#00ff00'),
    ('Обед', 'dinner', '#3b2fff'),
    ('Ужин', 'supper', '#8100EA'),
)


class Command(BaseCommand):
    help = 'Загрузка тестовых данных в БД'

    def handle(self, *args, **options):
        with open('data/ingredients.csv', encoding='utf-8') as cf:
            ingredients = csv.reader(cf)
            for item in ingredients:
                name, measurement_unit = item
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )

            # загрузка тегов
            for tag in TAGS:
                name, slug, color = tag
                Tag.objects.get_or_create(
                    name=name,
                    color=color,
                    slug=slug
                )
            return 'Данные успешно добавлены в таблицы Ingredient и Tag!'
