from typing import Tuple

from rest_framework import serializers, exceptions
from django.db import models, transaction

from core.models import User
from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


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

    def validate_board(self, value: Board) -> Board:
        """
        The validate_board function defines the serializer method. Takes an instance of Board as an argument.
        Checks the received data of the board field to create an instance of the class. Does not allow you to specify
        the board is marked as deleted and does not allow you to create a category on the board where the current user
        is not included in the list of allowed users and the role of the current user does not correspond
        to the editor or owner. Returns a verified instance of the board.
        """
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted board")

        try:
            _user: BoardParticipant = BoardParticipant.objects.get(user=self.context["request"].user, board=value.id)

        except BoardParticipant.DoesNotExist:
            raise serializers.ValidationError("only users with the owner or writers role can create categories")

        if _user.role not in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]:
            raise serializers.ValidationError("only users with the owner or writers role can create categories")

        return value


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
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "user", "board")


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

        try:
            _user: BoardParticipant = BoardParticipant.objects.get(user=self.context["request"].user, board=value.board)

        except BoardParticipant.DoesNotExist:
            raise exceptions.PermissionDenied("The user can create goals only in those categories in which "
                                              "he is a member of the boards with the role of Owner or Editor")

        if _user.role not in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]:
            raise exceptions.PermissionDenied("The user can create goals only in those categories in which "
                                              "he is a member of the boards with the role of Owner or Editor")

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

        try:
            _user = BoardParticipant.objects.get(user=self.context["request"].user, board__categories=value.category)
        except BoardParticipant.DoesNotExist:
            raise serializers.ValidationError("The user can create comments only for those goals in which "
                                              "he is a member of the boards with the role of Owner or Editor")

        if _user.role not in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]:
            raise serializers.ValidationError("The user can create comments only for those goals in which "
                                              "he is a member of the boards with the role of Owner or Editor")

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


class BoardCreateSerializer(serializers.ModelSerializer):
    """
    The BoardCreateSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the Board class when
    processing create new instance of Board class.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = Board
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated")
        fields: str = "__all__"

    def create(self, validated_data: dict) -> Board:
        """
        The create function overrides the method of the parent class. Takes the validated_data object as arguments.
        Creates an instance of the Board class and sets the current user as a board user with the owner role.
        Returns the created instance of the Board class.
        """
        user: User = validated_data.pop("user")
        board: Board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(user=user, board=board, role=BoardParticipant.Role.owner)
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    """
    The BoardParticipantSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the BoardParticipant class when
    processing usage instance of BoardParticipant class.
    """
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role)
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = BoardParticipant
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    """
    The BoardSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the Board class when
    processing usage instance of Board class.
    """
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = Board
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "created", "updated")

    def update(self, instance: Board, validated_data: dict) -> Board:
        """
        The update function overrides the method of the parent class. Takes as arguments an instance of the Board
        class and a validated_data object. Updates the data of an instance of the Board class in accordance with
        the received data. Returns an updated instance of the Board class.
        """
        owner: User = validated_data.pop("user")
        new_participants: list = validated_data.pop("participants")
        new_by_id: dict = {part["user"].id: part for part in new_participants}

        old_participants: list = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if old_participant.role != new_by_id[old_participant.user_id]["role"]:
                        old_participant.role = new_by_id[old_participant.user_id]["role"]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(board=instance, user=new_part["user"], role=new_part["role"])

            instance.title = validated_data["title"]
            instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    """
    The BoardListSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the Board class when
    processing usage instance of Board class.
    """
    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = Board
        fields: str = "__all__"
