from habit.paginators import CustomPaginator
from habit.models import Habit
from habit.serializers import HabitSerializer
from rest_framework import viewsets


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        """
        Выполняется проверка параметров запросов и если передан параметр public(True),
        то возвращаются только те привычки которые имеют флаг is_public=True.
        Если параметр public не передается, то возвращаются привычки, связанные с авторизованным пользователем.
        Каждый пользователь видит только свои привычки.
        """
        if self.action == 'list' and self.request.query_params.get('public'):
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        При создании привычки, привязываем к ней текущего пользователя.
        """
        serializer.save(user=self.request.user)
