from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, AccessRule, Role, Resource, Action

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    middle_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'password', 'password_confirm')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            middle_name=validated_data.get('middle_name', '')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'middle_name')
        read_only_fields = ('email',)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные или аккаунт удален.")

class AccessRuleSerializer(serializers.ModelSerializer):

    role_name = serializers.CharField(source='role.name', read_only=True)
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    action_name = serializers.CharField(source='action.name', read_only=True)

    class Meta:
        model = AccessRule
        fields = ['id', 'role', 'role_name', 'resource', 'resource_name', 'action', 'action_name', 'is_allowed']