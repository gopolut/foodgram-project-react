from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE = "user"
ADMIN_ROLE = "admin"

ROLE_CHOICES = (
    (USER_ROLE, "Пользователь"),
    (ADMIN_ROLE, "Администратор"),
)


class CustomUser(AbstractUser):
    """Кастомный класс юзера."""

    username = models.CharField(
        max_length=200,
        verbose_name="Пользователь",
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        max_length=200,
        verbose_name="Имя",
        blank=False,
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name='Фамилия',
        blank=False,
    )
    email = models.EmailField(
        max_length=200,
        verbose_name="Email address",
        blank=False, unique=True,
    )
    role = models.CharField(
        max_length=50,
        verbose_name="Роль",
        choices=ROLE_CHOICES,
        null=False,
        default=USER_ROLE,
    )
    is_active = models.BooleanField(
        verbose_name='Пользователь активен',
        default=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
