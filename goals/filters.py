from typing import Dict, Tuple

import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models import Goal


class GoalDateFilter(rest_framework.FilterSet):
    """
    The GoalDateFilter class inherits from the FilterSet class. Defines filtering settings based on request parameters.
    """
    class Meta:
        """
        The Meta class contains service information. Defines the fields of the model and the applicable type
        of filtering results for these fields.
        """
        model: models.Model = Goal
        fields: Dict[str, Tuple[str, ...]] = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }
