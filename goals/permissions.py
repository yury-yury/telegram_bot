from rest_framework import permissions

from goals.models import BoardParticipant, Board, GoalCategory, Goal, GoalComment


class BoardPermissions(permissions.BasePermission):
    """
    The BoardPermissions class inherits from the BasePermission class from the permissions module
    of the rest_framework library. Controls access to protected endpoints.
    """
    def has_object_permission(self, request, view, obj: Board) -> bool:
        """
        The has_object_permission function is a method of the BoardPermissions class. Accepts request, view,
        and an instance of the Board class as arguments. Checks the authentication of the current user.
        When requested by the method included in SAFE_METHODS, it checks that the current user is included
        in the list of users of this board. When requesting an unsafe method, the compliance of the user's role
        on this board with the role of editor or owner is additionally checked. If the test result is positive,
        it returns True, otherwise False.
        """
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj).exists()

        return BoardParticipant.objects.filter(user=request.user, board=obj,
                                               role=BoardParticipant.Role.owner).exists()


class CategoryPermissions(permissions.BasePermission):
    """
    The CategoryPermissions class inherits from the BasePermission class from the permissions module
    of the rest_framework library. Controls access to protected endpoints.
    """
    def has_object_permission(self, request, view, obj: GoalCategory) -> bool:
        """
        The has_object_permission function is a method of the CategoryPermissions class. Accepts request, view,
        and an instance of the GoalCategory class as arguments. Checks the authentication of the current user.
        When requested by the method included in SAFE_METHODS , it checks that the current user is included
        in the list of users of the board that this category belongs to . When requesting an unsafe method,
        the compliance of the user's role on the board with the role of editor or owner is additionally checked.
        If the test result is positive, it returns True, otherwise False.
        """
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.board).exists()

        else:
            _user = BoardParticipant.objects.filter(user=request.user, board=obj.board).get()
            return _user.role in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]


class GoalPermissions(permissions.BasePermission):
    """
    The GoalPermissions class inherits from the BasePermission class from the permissions module
    of the rest_framework library. Controls access to protected endpoints.
    """
    def has_object_permission(self, request, view, obj: Goal) -> bool:
        """
        The has_object_permission function is a method of the GoalPermissions class. Accepts request, view,
        and an instance of the Goal class as arguments. Checks the authentication of the current user.
        When requested by the method included in SAFE_METHODS, it checks that the current user is included in the list
        of users of the board that includes the category containing this goal. When requesting an unsafe method,
        the compliance of the user's role on the board with the role of editor or owner is additionally checked.
        If the test result is positive, it returns True, otherwise False.
        """
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board__categories=obj.category).exists()

        _user = BoardParticipant.objects.get(user=request.user, board__categories=obj.category)
        return _user.role in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]


class CommentPermissions(permissions.BasePermission):
    """
    The CommentPermissions class inherits from the BasePermission class from the permissions module
    of the rest_framework library. Controls access to protected endpoints.
    """
    def has_object_permission(self, request, view, obj: GoalComment) -> bool:
        """
        The has_object_permission function is a method of the CommentPermissions class. Accepts request, view,
        and an instance of the Comment class as arguments. Checks the authentication of the current user.
        When requested by the method included in SAFE_METHODS, it checks that the current user is included
        in the list of users of the board, which includes a category containing a goal for which a comment is written.
        When requesting an unsafe method, it is checked that the current user is the author of the comment.
        If the test result is positive, it returns True, otherwise False.
        """
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board__category__goal=obj.goal).exists()

        return obj.user == request.user
