from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs):
        data = super().validate(attrs)
        # data['password'] = self.validated_data['password']
        validate_password(data['password'])
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError('The entered passwords must match')
        del data['password_repeat']
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
