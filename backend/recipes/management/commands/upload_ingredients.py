import csv
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


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
            
            return 'Данные успешно добавлены в таблицу Ingredient!'
