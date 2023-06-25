from typing import Dict, Any
import pytest
from rest_framework.fields import DateTimeField

from goals.models import BoardParticipant, Goal, GoalCategory


@pytest.mark.django_db()
class TestGoalCreate:
    """
    The TestGoalCreate class combines all unit tests to check the functioning of the application when accessing
    the endpoint "/goals/goal/create" using the pytest library.
    """
    url: str = '/goals/goal/create'

    def test_goal_create_without_authorization(self, client) -> None:
        """
        The test_goal_create_without_authorization function is a test method. Takes as an argument an instance
        of the test client. Makes a POST request to the URL '/goals/goal/create' on behalf of a user
        who does not have authentication. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        response = client.post(self.url)

        assert response.status_code == 401
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_goal_create_on_board_for_not_participant(self, auth_client, goal_category: GoalCategory, faker) -> None:
        """
        The test_goal_create_on_board_for_not_participant function is a test method. Accepts as arguments the following
        instances authorized test client, GoalCategory and faker. Performs the creation of test data. Makes
        a POST request to the URL '/goals/goal/create' to create an instance of Goal on the board where the user
        is not a participant. Checks the compliance of the status code and the content of the application response.
        If there is a discrepancy, raises an exception.
        """
        data: Dict[str, Any] = {'category': goal_category.id, 'title': faker.sentence()}
        response = auth_client.post(self.url, data=data)

        assert response.status_code == 403
        assert response.json() == {'detail': 'The user can create goals only in those categories in which he is ' \
                                             'a member of the boards with the role of Owner or Editor'}

    def test_goal_create_on_board_for_reader(self, auth_client, goal_category: GoalCategory,
                                             board_participant: BoardParticipant, faker) -> None:
        """
        The test_goal_create_on_board_for_reader function is a test method. Accepts as arguments the following
        instances authorized test client, GoalCategory, GoalParticipant and faker. Performs the creation of test data.
        Makes a POST request to the URL '/goals/goal/create' to create an instance of Goal on the board where
        the user has the role of reader. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        board_participant.role = BoardParticipant.Role.reader
        board_participant.save(update_fields=['role'])

        data: Dict[str, Any] = {'category': goal_category.id, 'title': faker.sentence()}
        response = auth_client.post(self.url, data=data)

        assert response.status_code == 403
        assert response.json() == {'detail': 'The user can create goals only in those categories in which he is ' \
                                             'a member of the boards with the role of Owner or Editor'}

    @pytest.mark.parametrize('role', [BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                             ids=['owner', 'writer'])
    def test_goal_create_on_board_for_owner_or_writer(self, auth_client, goal_category: GoalCategory,
                                                      board_participant: BoardParticipant, faker, role) -> None:
        """
        The test_goal_create_on_board_for_owner_or_writer function is a parameterized test method. Accepts as arguments
        the following instances authorized test client, Goal Category, GoalParticipant, faker and role.
        Performs the creation of test data. Makes a POST request to the URL '/goals/goal/create' to create
        an instance of Goal on the board where the user has the role of owner or writer. Checks the compliance
        of the status code and the content of the application response. If there is a discrepancy, raises an exception.
        """
        board_participant.role = role
        board_participant.save(update_fields=['role'])

        data = {'category': goal_category.id, 'title': faker.sentence()}
        response = auth_client.post(self.url, data=data)
        new_goal: Goal = Goal.objects.get()

        assert response.status_code == 201
        assert response.json() == _serializer_response(new_goal)

    def test_goal_create_for_not_existing_category(self, auth_client, faker) -> None:
        """
        The test_goal_create_for_not_existing_category function is a test method. Accepts as arguments the following
        instances authorized test client, and faker. Performs the creation of test data. Makes a POST request
        to the URL '/goals/goal/create' to create an instance of Goal on a non-existent board. Checks the compliance
        of the status code and the content of the application response. If there is a discrepancy, raises an exception.
        """
        data: Dict[str, Any] = {'category': 2, 'title': faker.sentence()}
        response = auth_client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {'category': ['Invalid pk "2" - object does not exist.']}

    def test_goal_create_on_is_deleted_category(self, auth_client, goal_category: GoalCategory, faker) -> None:
        """
        The test_goal_create_on_is_deleted_category function is a test method. Accepts as arguments the following
        instances authorized test client, GoalCategory and faker. Performs the creation of test data.
        Makes a POST request to the URL '/goals/goal/create' to create an instance of Goal in the category
        marked as deleted. Checks the compliance of the status code and the content of the application response.
        If there is a discrepancy, raises an exception.
        """
        goal_category.is_deleted = True
        goal_category.save(update_fields=['is_deleted'])

        data: Dict[str, Any] = {'category': goal_category.id, 'title': faker.sentence()}
        response = auth_client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {'category': ['not allowed in deleted category']}


def _serializer_response(goal: Goal, **kwargs) -> dict:
    """
    The _serializer_response function takes as parameters an object of the Goal class and other named arguments.
    It is a serializer for representing an object of the Goal class in the form of a dictionary, where the names
    of fields in the form of strings act as keys, and the values of these fields act as values.
    Returns a dictionary compiled from the received instance of the class.
    """
    data: Dict[str, Any] = {'id': goal.id,
                            'created': DateTimeField().to_representation(goal.created),
                            'updated': DateTimeField().to_representation(goal.updated),
                            'title': goal.title,
                            'description': goal.description,
                            'status': goal.status,
                            'priority': goal.priority,
                            'due_date': DateTimeField().to_representation(goal.due_date),
                            'is_deleted': goal.is_deleted,
                            'category': goal.category.id
                            }
    return data | kwargs
