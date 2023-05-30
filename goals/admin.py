from typing import Tuple

from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    """
    The GoalCategoryAdmin class inherits from the ModelAdmin class. Defines the output of instance fields
    to the administration panel and the ability to edit them.
    """
    list_display: Tuple[str] = ("title", "user", "created", "updated")
    readonly_fields: Tuple[str] = ("created", "updated")
    search_fields: Tuple[str] = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    """
    The GoalAdmin class inherits from the ModelAdmin class. Defines the output of instance fields to the administration
    panel and the ability to edit them.
    """
    list_display: Tuple[str] = ("title", "user", "created", "updated", "category", "description", "status", "priority",
                                "due_date")
    readonly_fields: Tuple[str] = ("created", "updated")
    search_fields: Tuple[str] = ("title", "user", "category", "description", "status", "priority", "due_date")


class GoalCommentAdmin(admin.ModelAdmin):
    """
    The GoalCommentAdmin class inherits from the ModelAdmin class. Defines the output of instance fields
    to the administration panel and the ability to edit them.
    """
    list_display: Tuple[str] = ("user", "created", "updated", "goal", "text")
    readonly_fields: Tuple[str] = ("created", "updated")
    search_fields: Tuple[str] = ("user", "goal", "text")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
