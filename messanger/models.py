from django.db import models
from django.utils import timezone

from users.models import User


class SentMessage(models.Model):
    """

    """
    created = models.DateTimeField(verbose_name="Дата создания")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец сообщения")
    content = models.TextField(verbose_name="текст сообщения")

    def save(self, *args, **kwargs):
        """
        The save function adds additional functionality to the method of the parent class. Automatically fills
        in field when creating instances of the class. After that, it calls the method of the parent class.
        """
        if not self.id:
            self.created = timezone.now()

        return super().save(*args, **kwargs)

    class Meta:
        """
        The Meta class contains the common name of the model instance in the singular and plural used
        in the administration panel.
        """
        verbose_name: str = "Сообщение"
        verbose_name_plural: str = "Сообщения"

