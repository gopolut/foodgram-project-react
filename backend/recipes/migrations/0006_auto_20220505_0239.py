# Generated by Django 2.2.27 on 2022-05-04 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20220505_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(choices=[('#E26C2D', 'Оранжевый'), ('#00ff00', 'Зеленый'), ('#3b2fff', 'Синий'), ('#540099', 'Фиолетовый')], max_length=7, verbose_name='Цвет тега'),
        ),
    ]
