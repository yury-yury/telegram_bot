from typing import Tuple

from rest_framework import serializers
from django.db import models

from messanger.models import SentMessage
from users.serializers import UserSerializer


class SentMessageSerializer(serializers.ModelSerializer):
    """
    The SentMessageSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the SentMessage class when
    processing usage instance of SentMessage class.
    """
    owner = UserSerializer(read_only=True)

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = SentMessage
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "owner")
