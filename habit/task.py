from celery import shared_task
from django.utils import timezone
import requests
from habit.models import Habit
from users.models import CustomUser
from config import settings
import logging

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
            logger.warning(f'У пользователя {user.email} не привязан Telegram')
            return

        message = (
            f"⏰ Напоминание о привычке!\n"
            f"▶ Действие: {habit.action}\n"
            f"⏱ Время: {habit.time.strftime('%H:%M')}\n"
            f"📍 Место: {habit.place}\n"
            f"⏳ Длительность: {habit.duration} сек"
        )

        bot_token = settings.TELEGRAM_BOT_TOKEN
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        data = {
            'chat_id': user.telegram_chat_id,
            'text': message,
            'parse_mode': 'Markdown',
        }

        response = requests.post(url, data=data)
        response.raise_for_status()

    except Exception as e:
        logger.error(f'Ошибка отправки в Telegram: {str(e)}')


@shared_task
def check_habits_for_reminders():
    now = timezone.now()
    current_time = now.time().replace(second=0, microsecond=0)

    # Убедимся, что запрос отсортирован правильно, чтобы избежать ошибки с DISTINCT ON
    habits = Habit.objects.filter(time=current_time).select_related('user').order_by('user_id', 'time')

    for habit in habits:
        if not habit.user.telegram_chat_id:
            continue

        last_completed = habit.completions.order_by('-date').first()
        if last_completed:
            days_passed = (now.date() - last_completed.date).days
            if days_passed < habit.periodicity:
                continue

        send_telegram_reminder.delay(habit.id, habit.user.id)
