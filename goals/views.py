from typing import List

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import serializers
from django.db import models, transaction

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment
from goals.serializer import GoalCreateSerializer, GoalCategorySerializer, GoalCategoryCreateSerializer, GoalSerializer
from goals.serializer import GoalCommentCreateSerializer, GoalCommentSerializer


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
    ]
    ordering_fields: List[str] = ["title", "created"]
    ordering: List[str] = ["title"]
    search_fields: List[str] = ["title"]

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class for which
        the current user is the author and which have the value False in the is_deleted field.
        """
        return GoalCategory.objects.select_related('user').filter(user=self.request.user).exclude(is_deleted=True)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """
    The GoalCategoryView class inherits from the RetrieveUpdateDestroyAPIView class from the rest_framework.generics
    module and is a class-based view for processing requests with GET, PUT, PATCH and DELETE methods at the address
    '/goals/goal_category/<pk>'.
    """
    model: models.Model = GoalCategory
    serializer_class: serializers.ModelSerializer = GoalCategorySerializer
    permission_classes: list = [permissions.IsAuthenticated]

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class for which
        the current user is the author and which have the value False in the is_deleted field.
        """
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

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
        return Goal.objects.select_related('user').filter(user=self.request.user,
                                                          is_deleted=False).exclude(is_deleted=True)


class GoalView(RetrieveUpdateDestroyAPIView):
    """
    The GoalView class inherits from the RetrieveUpdateDestroyAPIView class from the rest_framework.generics
    module and is a class-based view for processing requests with GET, PUT, PATCH and DELETE methods at the address
    '/goals/goal/<pk>'.
    """
    model: models.Model = Goal
    serializer_class: serializers.ModelSerializer = GoalSerializer
    permission_classes: list = [permissions.IsAuthenticated]

    def get_queryset(self) -> list:
        """
        The get_queryset function overrides the method of the parent class. Does not accept parameters as arguments
        except for the instance itself. Returns a selection from the database of all instances of the class for which
        the current user is the author and which have the value False in the is_deleted field.
        """
        return Goal.objects.filter(user=self.request.user, is_deleted=False)

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
        return GoalComment.objects.select_related('user').filter(user=self.request.user).exclude(is_deleted=True)


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
