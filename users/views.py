from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from tutorial.quickstart.serializers import UserSerializer
from rest_framework import generics

from users.serializers import RegisterSerializer

User = get_user_model()  # Получаем модель пользователя


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Авторизованный пользоватеть


class RegisterView(generics.CreateAPIView):  # Позволяет создавать нового пользователя (зарегистрировать) POST
    queryset = User.objects.all()
    serializer_class = RegisterSerializer  # хэширование пароля при помощи RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Доступ без авторизации. Для регистрации.
