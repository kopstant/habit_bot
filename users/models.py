from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    email = models.EmailField(unique=True)
    telegram_chat_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telegram Chat ID',
    )
    # Произведена замена основного поля для регистрации. Теперь это емаил.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = ' Пользователи'

    def __str__(self):
        return f'{self.email}, {self.telegram_chat_id}'
