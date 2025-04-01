from datetime import datetime, date, time
from unittest.mock import patch
from django.db import connection

from django.test import TestCase
from django.utils import timezone
from habit.models import Completion, Habit
from habit.tasks import check_habits_for_reminders
from users.models import CustomUser


class CheckHabitReminderTaskTest(TestCase):
    def setUp(self):
        # Очистка базы данных перед каждым тестом
        connection.queries.clear()

        # Удаляем все привычки и completions перед каждым тестом
        Habit.objects.all().delete()
        Completion.objects.all().delete()

        # Создаём пользователя
        self.user = CustomUser.objects.create_user(
            email='check@user.com',
            username='checkuser',
            password='12345',
            telegram_chat_id='987654321'
        )

        # Устанавливаем фиксированное время для теста (убираем возможное дублирование)
        self.fixed_time = time(8, 0)

        # Создаём одну привычку
        self.habit = Habit.objects.create(
            user=self.user,
            place='дома',
            time=self.fixed_time,
            action='разминаться',
            duration=20,
            periodicity=1
        )

    @patch('habit.tasks.datetime')
    @patch('habit.tasks.send_telegram_reminder.delay')
    def test_habit_reminder_sent(self, mock_send_reminder, mock_datetime):
        from datetime import datetime, date, time, timedelta

        # Мокаем время
        mock_now = datetime.combine(date.today(), time(8, 0))
        mock_datetime.now.return_value = mock_now

        # Создаём completion "вчера"
        Completion.objects.create(
            habit=self.habit,
            date=date.today() - timedelta(days=1)
        )

        check_habits_for_reminders()

        mock_send_reminder.assert_called_once_with(self.habit.id, self.user.id)

    @patch('habit.tasks.send_telegram_reminder.delay')
    def test_habit_reminder_skipped_if_not_due(self, mock_send_reminder):
        """Уведомление не отправляется, если периодичность не выполнена"""
        Completion.objects.create(
            habit=self.habit,
            date=timezone.now().date()
        )

        check_habits_for_reminders()

        mock_send_reminder.assert_not_called()

    @patch('habit.tasks.datetime')
    @patch('habit.tasks.send_telegram_reminder.delay')
    def test_habit_reminder_sent_on_first_run(self, mock_send_reminder, mock_datetime):
        """Уведомление отправляется, если у привычки нет записей в Completion (первый запуск)"""
        # Мокаем время
        mock_now = datetime.combine(date.today(), time(8, 0))
        mock_datetime.now.return_value = mock_now

        # Используем self.habit из setUp, а не создаём новую
        habit_id = self.habit.id

        # Запускаем задачу
        check_habits_for_reminders()

        # Проверяем, что уведомление отправилось 1 раз для self.habit
        mock_send_reminder.assert_called_once_with(habit_id, self.user.id)
