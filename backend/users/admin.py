from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # фильтрация
    list_filter = (
        'username',
        'email',
    )
    
    search_fields = (
        'username',
    )
