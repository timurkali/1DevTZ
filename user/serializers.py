from datetime import datetime

from django.contrib.auth import get_user_model, authenticate, password_validation
from rest_framework import serializers

from user import models

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate_password(self, password):
        password_validation.validate_password(password=password)
        return password

    def create(self, validated_data):
        validated_data['last_login'] = datetime.now()
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        models.Wallet(user=user).save()

        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'token')


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError({'username': 'Incorrect username or password.'})

        return user
