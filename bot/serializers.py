from typing import Tuple
from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    """
    The TgUserSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the TgUser class when
    processing usage instance of TgUser class.
    """
    tg_id = serializers.IntegerField(source='chat_id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    verification_code = serializers.CharField(write_only=True)

    def validate_verification_code(self, code: str) -> str:
        """
        The validate_verification_code function defines a class method. Accepts the verification code sent
        by the user as a parameter. Makes a request from the database of the user who has the corresponding code.
        Sets the found user as the current one. Otherwise, raises a ValidationError exception. Returns
        the received code as a string.
        """
        try:
            tg_user: TgUser = TgUser.objects.get(verification_code=code)
        except TgUser.DoesNotExist:
            raise ValidationError('Invalid verification code')
        else:
            if tg_user.is_verified:
                raise ValidationError('Unsupported error')
            self.instance = tg_user
            return code

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = TgUser
        fields: Tuple[str, ...] = ('tg_id', 'username', 'user_id', 'verification_code')
