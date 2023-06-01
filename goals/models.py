from typing import List, Tuple

from django.db import models
from django.utils import timezone

from core.models import User


class DatesModelMixin(models.Model):
    """
    The DatesModelMixin class inherits from the Model class. Is an abstract class. Contains fields and methods common
    to all goals application models.
    """
    class Meta:
        """
        The Meta class contains the designation of an abstract class to instruct the Django framework not to create
        a separate table in the database.
        """
        abstract: bool = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        """
        The save function adds additional functionality to the method of the parent class. Automatically fills
        in fields when creating and editing instances of the class. After that, it calls the method of the parent class.
        """
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class Board(DatesModelMixin):
    """
    The Board class inherits from the abstract DatesModelMixin class. Defines the database table fields
    and their properties.
    """
    class Meta:
        """
        The Meta class contains the common name of the model instance in the singular and plural used
        in the administration panel.
        """
        verbose_name: str = "Доска"
        verbose_name_plural: str = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class BoardParticipant(DatesModelMixin):
    """
    The BoardParticipant class inherits from the abstract DatesModelMixin class. Defines the database table fields
    and their properties.
    """
    class Meta:
        """
        The Meta class contains the common name of the model instance in the singular and plural used
        in the administration panel.
        """
        unique_together: Tuple[str, ...] = ("board", "user")
        verbose_name: str = "Участник"
        verbose_name_plural: str = "Участники"

    class Role(models.IntegerChoices):
        """
        The Role class inherits from the Integer Choices class from the django.db.models module. Contains possible
        numeric values and their designations for filling in the role field of the BoardParticipant model.
        """
        owner: Tuple[int, str] = 1, "Владелец"
        writer: Tuple[int, str] = 2, "Редактор"
        reader: Tuple[int, str] = 3, "Читатель"

    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="participants")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="participants")
    role = models.PositiveSmallIntegerField(verbose_name="Роль", choices=Role.choices, default=Role.owner)


class GoalCategory(DatesModelMixin):
    """
    The GoalCategory class inherits from the abstract DatesModelMixin class. Defines the database table fields
    and their properties.
    """
    class Meta:
        """
        The Meta class contains the common name of the model instance in the singular and plural used
        in the administration panel.
        """
        verbose_name: str = "Категория"
        verbose_name_plural: str = "Категории"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Название", max_length=255)
    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(DatesModelMixin):
    """
    The Goal class inherits from the abstract DatesModelMixin class. Defines the database table fields
    and their properties.
    """
    class Meta:
        """
        The Meta class contains the common name of the model instance in the singular and plural used
        in the administration panel.
        """
        verbose_name: str = "Цель"
        verbose_name_plural: str = "Цели"

    class Status(models.IntegerChoices):
        """
        The Status class inherits from the Integer Choices class from the django.db.models module. Contains possible
        numeric values and their designations for filling in the status field of the Goal model.
        """
        to_do: Tuple[int, str] = 1, "К выполнению"
        in_progress: Tuple[int, str] = 2, "В процессе"
        done: Tuple[int, str] = 3, "Выполнено"
        archived: Tuple[int, str] = 4, "Архив"

    class Priority(models.IntegerChoices):
        """
        The Priority class inherits from the Integer Choices class from the django.db.models module. Contains possible
        numeric values and their designations for filling in the priority field of the Goal model.
        """
        low: Tuple[int, str] = 1, "Низкий"
        medium: Tuple[int, str] = 2, "Средний"
        high: Tuple[int, str] = 3, "Высокий"
        critical: Tuple[int, str] = 4, "Критический"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, on_delete=models.CASCADE, verbose_name="Категория")
    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Priority.choices,
                                                default=Priority.medium)
    due_date = models.DateField(verbose_name="Дата дедлайна", null=True)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class GoalComment(DatesModelMixin):
    """
    The GoalComment class inherits from the abstract DatesModelMixin class. Defines the database table fields
    and their properties.
    """
    class Meta:
        """
        The Meta class contains the general singular and plural name of the model instance used in the administration
        panel, as well as an indication of the sorting order of the results in the list of class instances.
        """
        verbose_name: str = "Комментарий"
        verbose_name_plural: str = "Комментарии"
        ordering: List[str] = ["-created"]

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    text = models.TextField(verbose_name="Текст")
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, verbose_name="Цель")
