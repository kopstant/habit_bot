from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Habit(models.Model):
    PERIODICITY_CHOICES = [
        (1, "Ежедневно"),
        (2, "Каждые 2 дня"),
        (3, "Каждые 3 дня"),
        (4, "Каждые 4 дня"),
        (5, "Каждые 5 дней"),
        (6, "Каждые 6 дней"),
        (7, "Еженедельно"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность",
    )
    reward = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Вознаграждение"
    )
    duration = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name="Время на выполнение (в секундах)",
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]


class Completion(models.Model):  # Для теста
    habit = models.ForeignKey(
        Habit,
        related_name="completions",
        on_delete=models.CASCADE,
    )
    date = models.DateField()
