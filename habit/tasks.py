from celery import shared_task
from django.utils import timezone
import requests
from habit.models import Habit
from users.models import CustomUser
from config import settings
import logging
from datetime import datetime
from django.apps import apps
from .services import send_telegram_message

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_reminder(habit_id, user_id):
    """
    Напоминание о привычке
    """
    try:
        habit = Habit.objects.get(id=habit_id)
        user = CustomUser.objects.get(id=user_id)

        if not user.telegram_chat_id:
            logger.warning(f"У пользователя {user.email} не привязан Telegram")
            return

        message = (
            f"⏰ Напоминание о привычке!\n"
            f"▶ Действие: {habit.action}\n"
            f"⏱ Время: {habit.time.strftime('%H:%M')}\n"
            f"📍 Место: {habit.place}\n"
            f"⏳ Длительность: {habit.duration} сек"
        )

        bot_token = settings.TELEGRAM_BOT_TOKEN
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": user.telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }

        response = requests.post(url, data=data)
        response.raise_for_status()

    except Exception as e:
        logger.error(f"Ошибка отправки в Telegram: {str(e)}")


@shared_task
def check_habits_for_reminders():
    """
    Проверяет привычки и отправляет напоминания через Telegram
    """
    # Получаем модель Habit только когда приложение готово
    Habit = apps.get_model("habit", "Habit")

    current_time = datetime.now()

    # Получаем все привычки, которые нужно проверить
    habits = Habit.objects.filter(
        time__hour=current_time.hour, time__minute=current_time.minute
    )

    for habit in habits:
        if habit.user.telegram_chat_id:
            send_telegram_reminder.delay(habit.id, habit.user.id)
