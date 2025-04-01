from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'telegram_chat_id': {'required': False},
        }


class RegisterSerializer(serializers.ModelSerializer):  # Сериализатор для создания новых пользователей
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
        ]

    def create(self, validated_data):
        """
        Создает пользователя, используется встроенный метод Django(для хеширования пароля).
        return:: Созданный пользователь
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
