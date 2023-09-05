from django.db import models
from rest_framework import permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination

from bot.models import TgUser
from bot.tg.client import TgClient
from messanger.models import SentMessage
from messanger.serializers import SentMessageSerializer


class SentMessageView(ListCreateAPIView):
    model: models.Model = SentMessage
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = SentMessageSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer) -> None:
        """
        The perform_create function overrides the parent class method.
        Sets the value of the owner field.
        """
        message = serializer.save(owner=self.request.user)
        try:
            client = TgUser.objects.get(user=self.request.user)
        except TgUser.DoesNotExist:
            raise ValidationError("User is not verification")

        text:str = f"{self.request.user.username}, я получил от тебя сообщение: \n {message.content}"
        TgClient().send_message(chat_id=client.chat_id, text=text)

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances
        of the class created by the current user.
        """
        return SentMessage.objects.filter(owner=self.request.user)
