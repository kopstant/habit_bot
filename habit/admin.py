from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "telegram_chat_id", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "username", "telegram_chat_id")
    ordering = ("email",)
