from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
    )

    list_filter = (
        'username',
        'email',
    )
    
    search_fields = (
        'username',
    )
