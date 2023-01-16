from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from core.models import User


class SignUpSerializer(serializers.ModelSerializer):
    """Создание пользователя"""
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=True, max_length=50)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(required=True)

    def is_valid(self, raise_exception=False) -> bool:
        self._password_repeat = self.initial_data.pop('password_repeat')
        return super().is_valid(raise_exception=raise_exception)

    def validate_username(self, value: str) -> str:
        if self.Meta.model.objects.filter(username=value).exists():
            raise serializers.ValidationError(['User with such username already exists'])
        return value

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def validate(self, data: dict) -> dict:
        if data.get('password') != self._password_repeat:
            raise serializers.ValidationError({'password_repeat': ['Passwords must match']})
        return data

    def create(self, validated_data: dict) -> User:
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']


class RetrieveUpdateSerializer(serializers.ModelSerializer):
    """Просмотр, редактирование, удаление профиля"""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False, max_length=50)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UpdatePasswordSerializer(serializers.Serializer):
    """Изменение пароля"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    @staticmethod
    def validate_new_password(value: str) -> str:
        validate_password(value)
        return value


class LoginSerializer(serializers.ModelSerializer):
    """Авторизация пользователя"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data: dict) -> User:
        if not (user := authenticate(
                username=validated_data['username'],
                password=validated_data['password']
        )):
            raise AuthenticationFailed
        return user
