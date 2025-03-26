from rest_framework import serializers
from habit.models import Habit
from django.core.exceptions import ValidationError


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        """
        Валидация данных для привычки:
        - Исключить одновременный выбор связанной привычки и указания вознаграждения
        - В связанные привычки могут попадать только привычки с признаком приятной привычки
        - У приятной привычки не может быть вознаграждения или связанной привычки
        """
        if data.get('related_habit') and data.get('reward'):
            raise serializers.ValidationError(
                "Нельзя указывать одновременно связанную привычку и вознаграждение."
            )
        if data.get('related_habit'):
            related_habit = data['related_habit']
            if not related_habit.is_pleasant:
                raise serializers.ValidationError(
                    "В связанные привычки могут попадать только приятные привычки."
                )
        if data.get('is_pleasant', False):
            if data.get('reward') or data.get('related_habit'):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )

        return data
