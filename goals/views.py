from typing import List

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import serializers
from django.db import models, transaction

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from goals.permissions import BoardPermissions, CategoryPermissions, GoalPermissions
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, GoalCategoryCreateSerializer, GoalSerializer, \
    BoardCreateSerializer, BoardSerializer, BoardListSerializer
from goals.serializers import GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCategoryCreateView(CreateAPIView):
    """
    The GoalCategoryCreateView class inherits from the CreateAPIView class from the rest_framework.generics module
    and is a class-based view for processing requests with POST methods at the address '/goals/goal_category/create'.
    """
    model: models.Model = GoalCategory
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """
    The GoalCategoryListView class inherits from the Listview class from the rest_framework module.generics
    and is a class-based representation for processing requests by GET methods at the address
    '/goals/goal_category/list'. Contains the necessary information for organizing data filtering and sorting.
    """
    model: models.Model = GoalCategory
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends: list = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields: List[str] = ["title", "created"]
    ordering: List[str] = ["title"]
    filterset_fields: List[str] = ["title", "board", "user"]

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class located
        on the boards where the current user is specified as a user and which have the value False in the is_deleted
        field.
        """
        return GoalCategory.objects.select_related('user').filter(
            board__participants__user=self.request.user).exclude(is_deleted=True)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """
    The GoalCategoryView class inherits from the RetrieveUpdateDestroyAPIView class from the rest_framework.generics
    module and is a class-based view for processing requests with GET, PUT, PATCH and DELETE methods at the address
    '/goals/goal_category/<pk>'.
    """
    model: models.Model = GoalCategory
    serializer_class: serializers.ModelSerializer = GoalCategorySerializer
    permission_classes: list = [permissions.IsAuthenticated, CategoryPermissions]

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class located
        on the boards where the current user is specified as a user and which have the value False in the is_deleted
        field.
        """
        return GoalCategory.objects.select_related('user').filter(
            board__participants__user=self.request.user).exclude(is_deleted=True)


    def perform_destroy(self, instance: GoalCategory) -> None:
        """
        The perform_destroy function overrides the method of the parent class. Takes as an argument an instance
        of the GoalCategory class. Sets the True value in the is_deleted field of the instance, and also sets this
        value for all instances of the Goal class that have a reference to the current category. Saves modified
        instances. Returns an instance of the GoalCategory class.
        """
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goal_set.update(status=Goal.Status.archived)


class GoalCreateView(CreateAPIView):
    """
    The GoalCreateView class inherits from the CreateAPIView class from the rest_framework.generics module
    and is a class-based view for processing requests with POST methods at the address '/goals/goal/create'.
    """
    model: models.Model = Goal
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalCreateSerializer


class GoalListView(ListAPIView):
    """
    The GoalListView class inherits from the Listview class from the rest_framework module.generics
    and is a class-based representation for processing requests by GET methods at the address '/goals/goal/list'.
    Contains the necessary information for organizing data filtering and sorting.
    """
    model: models.Model = Goal
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends: list = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields: List[str] = ["title", "created"]
    ordering: List[str] = ["title"]
    search_fields: List[str] = ["title", "description"]

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class for which
        the current user is the author and which have the value False in the is_deleted field.
        """
        return Goal.objects.select_related('user').filter(
            category__board__participants__user=self.request.user).exclude(is_deleted=True)


class GoalView(RetrieveUpdateDestroyAPIView):
    """
    The GoalView class inherits from the RetrieveUpdateDestroyAPIView class from the rest_framework.generics
    module and is a class-based view for processing requests with GET, PUT, PATCH and DELETE methods at the address
    '/goals/goal/<pk>'.
    """
    model: models.Model = Goal
    serializer_class: serializers.ModelSerializer = GoalSerializer
    permission_classes: list = [permissions.IsAuthenticated, GoalPermissions]

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class for which
        the current user is the author and which have the value False in the is_deleted field.
        """
        return Goal.objects.filter(category__board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Goal) -> None:
        """
        The perform_destroy function overrides the method of the parent class. Takes as an argument an instance
        of the Goal class. Sets the value to True in the is_deleted field of the instance. Saves the modified instance.
        Returns an instance of the Goal class.
        """
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(CreateAPIView):
    """
    The GoalCommentCreateView class inherits from the CreateAPIView class from the rest_framework.generics module
    and is a class-based view for processing requests with POST methods at the address '/goals/goal_comment/create'.
    """
    model: models.Model = GoalComment
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    """
    The GoalCommentListView class inherits from the Listview class from the rest_framework module.generics
    and is a class-based representation for processing requests by GET methods at the address
    '/goals/goal_comment/list'. Contains the necessary information for organizing data filtering and sorting.
    """
    model: models.Model = GoalComment
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends: list = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields: List[str] = ["text", "goal", "created", "updated"]
    filterset_fields: List[str] = ["goal"]

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class for which
        the current user is the author.
        """
        return GoalComment.objects.select_related('user').filter(
            goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    """
    The GoalCommentView class inherits from the RetrieveUpdateDestroyAPIView class from the rest_framework.generics
    module and is a class-based view for processing requests with GET, PUT, PATCH and DELETE methods at the address
    '/goals/goal_comment/<pk>'.
    """
    model: models.Model = GoalComment
    serializer_class: serializers.ModelSerializer = GoalCommentSerializer
    permission_classes: list = [permissions.IsAuthenticated]

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class for which
        the current user is the author.
        """
        return GoalComment.objects.filter(user=self.request.user)


class BoardCreateView(CreateAPIView):
    """
    The BoardCreateView class inherits from the CreateAPIView class from the rest_framework.generics module
    and is a class-based view for processing requests with POST methods at the address '/goals/board/create'.
    """
    model: models.Model = Board
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = BoardCreateSerializer


class BoardListView(ListAPIView):
    """
    The BoardListView class inherits from the Listview class from the rest_framework module.generics
    and is a class-based representation for processing requests by GET methods at the address
    '/goals/board/list'. Contains the necessary information for organizing data filtering and sorting.
    """
    model: models.Model = Board
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = BoardListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends: list = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields: List[str] = ["title", ]
    filterset_fields: List[str] = ["title", ]

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class for which
        the current user is the participant.
        """
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    """
    The BoardView class inherits from the RetrieveUpdateDestroyAPIView class from the rest_framework.generics
    module and is a class-based view for processing requests with GET, PUT, PATCH and DELETE methods at the address
    '/goals/board/<pk>'.
    """
    model: models.Model = Board
    permission_classes: list = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self) -> List[Board]:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class for which
        the current user is the participant.
        """
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board) -> None:
        """
        The perform_destroy function overrides the method of the parent class. Takes as an argument an instance
        of the Board class. Sets the value to True in the is_deleted field of the instance. We set the True value
        in the is_deleted field to all categories associated with the deleted board, and also change the status
        of the goals contained in the categories located on the deleted board to the Archive status. Saves the modified
        instance.
        """
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
