from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from habit.models import Habit
from datetime import time

from habit.serializers import HabitSerializer

User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpassword123"
        )
        self.register_url = reverse("users:register")
        self.user_list_url = reverse("users:user-list")
        self.bind_telegram_url = reverse("users:user-bind-telegram")

    def authenticate(self):
        """Авторизация пользователя через force_authenticate"""
        self.client.force_authenticate(user=self.user)

    def test_register_user(self):
        """Проверка регистрации нового пользователя"""
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_get_user_list_authenticated(self):
        """Проверка доступа к списку пользователей для авторизованного пользователя"""
        self.authenticate()
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user.email, str(response.data))

    def test_get_user_list_unauthenticated(self):
        """Проверка отказа в доступе к списку пользователей без авторизации"""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # было 403

    def test_bind_telegram_success(self):
        """Успешная привязка telegram_chat_id"""
        self.authenticate()
        data = {"telegram_chat_id": "987654321"}
        response = self.client.post(self.bind_telegram_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["telegram_chat_id"], "987654321")

    def test_bind_telegram_missing_chat_id(self):
        """Ошибка при отсутствии telegram_chat_id"""
        self.authenticate()
        response = self.client.post(self.bind_telegram_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_user_str_method(self):
        self.assertEqual(
            str(self.user), f"{self.user.email}, {self.user.telegram_chat_id}"
        )


class HabitSerializerValidationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", username="user", password="testpass"
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="дом",
            time=time(8, 0),
            action="читать",
            is_pleasant=True,
            duration=20,
        )

    def test_related_habit_and_reward_together(self):
        """Нельзя указывать связанную привычку и вознаграждение одновременно"""
        data = {
            "user": self.user.id,
            "place": "парк",
            "time": "09:00:00",
            "action": "бегать",
            "related_habit": self.pleasant_habit.id,
            "reward": "купить кофе",
            "duration": 15,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_related_habit_not_pleasant(self):
        """В связанные привычки можно добавлять только приятные"""
        non_pleasant = Habit.objects.create(
            user=self.user,
            place="улица",
            time=time(7, 0),
            action="отжиматься",
            is_pleasant=False,
            duration=15,
        )
        data = {
            "user": self.user.id,
            "place": "двор",
            "time": "10:00:00",
            "action": "приседать",
            "related_habit": non_pleasant.id,
            "duration": 15,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_pleasant_with_reward_or_related(self):
        """У приятной привычки не может быть вознаграждения или связанной привычки"""
        data = {
            "user": self.user.id,
            "place": "дом",
            "time": "06:30:00",
            "action": "медитировать",
            "is_pleasant": True,
            "reward": "посмотреть фильм",
            "duration": 15,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_valid_habit(self):
        """Корректная привычка проходит валидацию"""
        data = {
            "user": self.user.id,
            "place": "офис",
            "time": "11:00:00",
            "action": "встать и размяться",
            "duration": 10,
            "reward": "печенька",
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())
