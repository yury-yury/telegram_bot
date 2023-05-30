from typing import Tuple

from rest_framework import serializers
from django.db import models

from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, GoalComment


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """
    The GoalCategoryCreateSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the GoalCategory class when
    processing create new instance of GoalCategory class.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = GoalCategory
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")


class GoalCategorySerializer(serializers.ModelSerializer):
    """
    The GoalCategorySerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the GoalCategory class when
    processing usage instance of GoalCategory class.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = GoalCategory
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")


class GoalCreateSerializer(serializers.ModelSerializer):
    """
    The GoalCreateSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the Goal class when
    processing create new instance of Goal class.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = Goal
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")
        fields: str = "__all__"

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        """
        The validate_category function defines the serializer method. Takes an instance of a category as an argument.
        Checks the received data of the category field to create an instance of the class. Does not allow you to specify
        the category is marked as deleted and does not allow you to create a goal in a category created by another user.
        Is returning a verified instance of the category.
        """
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value


class GoalSerializer(serializers.ModelSerializer):
    """
    The GoalSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the Goal class when
    processing usage instance of Goal class.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = Goal
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    """
    The GoalCommentCreateSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the GoalComment class when
    processing create new instance of GoalComment class.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = GoalComment
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")
        fields: str = "__all__"

    def validate_goal(self, value: Goal) -> Goal:
        """
        The validate_goal function defines the serializer method. Accepts the instance of a goal as arguments.
        Checks the received data of the goal field to create an instance of the class. It does not allow the indication
        of a goal marked as deleted and does not allow the creation of a comment to a goal created by another user.
        Returns a validated instance of the goal.
        """
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted goal")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of goal")

        return value


class GoalCommentSerializer(serializers.ModelSerializer):
    """
    The GoalCommentSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the GoalComment class when
    processing usage instance of GoalComment class.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = GoalComment
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user")
