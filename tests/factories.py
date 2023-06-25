import factory.django
from django.db import models
from django.utils import timezone
from pytest_factoryboy import register

from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


@register
class UserFactory(factory.django.DjangoModelFactory):
    """
    The UserFactory class inherits from the parent class DjangoModelFactory from the factory.django module.
    It is intended for creating instances of the User class in order to conduct unit tests of the functioning
    of applications using the pytest library.
    """
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        """
        The Meta class is an internal utility class. Contains the name of the model for the purpose
        of creating test instances.
        """
        model: models.Model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> User:
        """
        The _create function overrides the protected class method of the parent class. Accepts the model_class
        object and all other positional and named arguments as parameters. Creates and returns an instance
        of the User class.
        """
        return User.objects.create(*args, **kwargs)


class DateFactoryMixin(factory.django.DjangoModelFactory):
    """
    The Date Factory Mix in class inherits from the parent DjangoModelFactory class from the factory.django module.
    It is intended for subsequent inheritance by classes of factories for creating test instances.
    Contains logic for creating common fields contained in each data model.
    """
    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)


@register
class BoardFactory(DateFactoryMixin):
    """
    The Board Factory class inherits from the parent DateFactoryMixin class. It is intended for creating instances
    of the Board class in order to conduct unit tests of the functioning of applications using the pytest library.
    """
    title = factory.Faker('sentence')

    class Meta:
        """
        The Meta class is an internal utility class. Contains the name of the model for the purpose
        of creating test instances.
        """
        model: models.Model = Board

    # @factory.post_generation
    # def with_owner(self, create, owner, **kwargs):
    #     if owner:
    #         BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


@register
class BoardParticipantFactory(DateFactoryMixin):
    """
    The BoardParticipantFactory class inherits from the parent DateFactoryMixin class. It is intended for creating
    instances of the BoardParticipant class in order to conduct unit tests of the functioning of applications using
    the pytest library.
    """
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        """
        The Meta class is an internal utility class. Contains the name of the model for the purpose
        of creating test instances.
        """
        model: models.Model = BoardParticipant


@register
class GoalCategoryFactory(DateFactoryMixin):
    """
    The GoalCategoryFactory class inherits from the parent DateFactoryMixin class. It is intended for creating
    instances of the GoalCategory class in order to conduct unit tests of the functioning of applications using
    the pytest library.
    """
    title = factory.Faker('catch_phrase')
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)

    class Meta:
        """
        The Meta class is an internal utility class. Contains the name of the model for the purpose
        of creating test instances.
        """
        model: models.Model = GoalCategory


@register
class GoalFactory(DateFactoryMixin):
    """
    The Goal Factory class inherits from the parent DateFactoryMixin class. It is intended for creating instances
    of the Goal class in order to conduct unit tests of the functioning of applications using the pytest library.
    """
    title = factory.Faker('catch_phrase')
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)

    class Meta:
        """
        The Meta class is an internal utility class. Contains the name of the model for the purpose
        of creating test instances.
        """
        model: models.Model = Goal


@register
class GoalCommentFactory(DateFactoryMixin):
    """
    The GoalCommentFactory class inherits from the parent DateFactoryMixin class. It is intended for creating
    instances of the GoalComment class in order to conduct unit tests of the functioning of applications using
    the pytest library.
    """
    text = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)

    class Meta:
        """
        The Meta class is an internal utility class. Contains the name of the model for the purpose
        of creating test instances.
        """
        model: models.Model = GoalComment
