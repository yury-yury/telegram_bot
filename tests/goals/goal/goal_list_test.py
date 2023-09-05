from typing import List, Any, Dict
import pytest

from users.models import User
from goals.models import Goal, Board, GoalCategory
from goals.serializers import GoalSerializer
from tests.factories import GoalFactory, GoalCategoryFactory, BoardParticipantFactory


@pytest.mark.django_db()
class TestGoalList:
    """
    The TestGoalList class combines all unit tests to check the functioning of the application when accessing
    the endpoint "/goals/goal/create" using the pytest library.
    """
    url: str = '/goals/goal/list'

    def test_goal_list_without_authorization(self, client) -> None:
        """
        The test_goal_list_without_authorization function is a test method. Takes as an argument an instance
        of the test client. Makes a GET request to the URL '/goals/goal/list' on behalf of a user
        who does not have authentication. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        response = client.get(self.url)

        assert response.status_code == 401
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_goal_list_true(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_true function is a test method. Accepts as arguments the following instances
        authorized test client, User and Board. Performs the creation of test data. Makes a GET request
        to the URL '/goals/goal/list' . Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        goals: List[Goal] = GoalFactory.create_batch(size=2, category=category)
        BoardParticipantFactory(board=board, user=user)

        expected_response: List[Dict[str, Any]] = GoalSerializer(goals, many=True).data
        expected_response.sort(key=lambda x: x["title"])

        response = auth_client.get(self.url)

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_goal_list_ordering_by_title(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_ordering_by_title function is a test method. Accepts the following instances
        as arguments: authorized test client, User and Board. Performs the creation of test data.
        Makes a GET request to the URL '/goals/goal/list?ordering=title' to issue a list of Goals
        ordered by the value of the 'title' field. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        goals: List[Goal] = GoalFactory.create_batch(size=2, category=category)
        BoardParticipantFactory(board=board, user=user)

        expected_response: List[Dict[str, Any]] = GoalSerializer(goals, many=True).data
        expected_response.sort(key=lambda x: x["title"])

        response = auth_client.get(self.url + '?ordering=title')

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_goal_list_ordering_by_created(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_ordering_by_title function is a test method. Accepts the following instances
        as arguments: authorized test client, User and Board. Performs the creation of test data.
        Makes a GET request to the URL '/goals/goal/list?ordering=created' to output a list of Goals
        ordered by the value of the 'created' field. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        goals: List[Goal] = GoalFactory.create_batch(size=2, category=category)
        BoardParticipantFactory(board=board, user=user)

        expected_response: List[Dict[str, Any]] = GoalSerializer(goals, many=True).data
        expected_response.sort(key=lambda x: x["created"])

        response = auth_client.get(self.url + '?ordering=created')

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_goal_list_with_limit(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_with_limit function is a test method. Accepts the following instances
        as arguments: authorized test client, User and Board. Performs the creation of test data.
        Makes a GET request to the URL '/goals/goal/list?limit=1' to output a list of Goal objects
        with pagination enabled with a limit of one object. Checks the compliance of the status code
        and the content of the application response. If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        goals: List[Goal] = GoalFactory.create_batch(size=2, category=category)
        BoardParticipantFactory(board=board, user=user)

        result: List[Dict[str, Any]] = GoalSerializer(goals, many=True).data
        result.sort(key=lambda x: x["title"])
        result.pop()
        expected_response: Dict[str, Any] = {'count': 2,
                                             'next': 'http://testserver/goals/goal/list?limit=1&offset=1',
                                             'previous': None,
                                             'results': result}

        response = auth_client.get(self.url + '?limit=1')

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_goal_list_with_limit_and_offset(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_with_limit_and_offset function is a test method. Accepts the following instances
        as arguments: authorized test client, User and Board. Performs the creation of test data.
        Makes a GET request to the URL '/goals/goal/list?limit=1&offset=1' to output a list of Goal objects
        with pagination enabled with a limit of one object with an offset of one object . Checks the compliance
        of the status code and the content of the application response. If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        goals: List[Goal] = GoalFactory.create_batch(size=2, category=category)
        BoardParticipantFactory(board=board, user=user)

        result: List[Dict[str, Any]] = GoalSerializer(goals, many=True).data
        result.sort(key=lambda x: x["title"])
        _result = list()
        _result.append(result.pop())
        expected_response: Dict[str, Any] = {'count': 2,
                                             'next': None,
                                             'previous': 'http://testserver/goals/goal/list?limit=1',
                                             'results': _result
                                             }

        response = auth_client.get(self.url + '?limit=1&offset=1')

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_goal_list_with_limit_and_offset_empty(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_with_limit_and_offset_empty function is a test method. Accepts the following instances
        as arguments: authorized test client, User and Board. Performs the creation of test data.
        Makes a GET request to the URL '/goals/goal/list?limit=1&offset=2' to output a list of Goal objects
        with pagination enabled with a limit of one object with an offset for the entire list of objects .
        Checks the compliance of the status code and the content of the application response.
        If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        GoalFactory.create_batch(size=2, category=category)
        BoardParticipantFactory(board=board, user=user)

        expected_response: Dict[str, Any] = {'count': 2,
                                             'next': None,
                                             'previous': 'http://testserver/goals/goal/list?limit=1&offset=1',
                                             'results': [],
                                             }

        response = auth_client.get(self.url + '?limit=1&offset=2')

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_goal_list_with_search(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_with_search function is a test method. Accepts the following instances as arguments:
        authorized test client, User and Board. Performs the creation of test data. Makes a GET request
        to the URL '/goals/goal/list?search=text' to output a list of Goal objects that have the specified
        search fragment in the value of the 'title' field. Checks the compliance of the status code
        and the content of the application response. If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        goals: List[Goal] = GoalFactory.create_batch(size=2, category=category)
        BoardParticipantFactory(board=board, user=user)

        result:List[Dict[str, Any]] = GoalSerializer(goals, many=True).data
        result.pop(1)

        response = auth_client.get(self.url + '?search=' + goals[0].title)

        assert response.status_code == 200
        assert response.json() == result

    def test_goal_list_with_priority(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_with_priority function is a test method. Accepts the following instances
        as arguments: authorized test client, User and Board. Performs the creation of test data.
        Makes a GET request to the URL '/goals/goal/list?priority=4' to output a list of Goal objects
        that have the specified value in the value of the 'priority' field. Checks the compliance
        of the status code and the content of the application response. If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        goals: List[Goal] = GoalFactory.create_batch(size=2, category=category)
        BoardParticipantFactory(board=board, user=user)
        goals[0].priority = Goal.Priority.critical
        goals[0].save(update_fields=['priority'])

        _goals: List[Goal] = [Goal.objects.get(id=goals[0].id)]
        result: List[Dict[str, Any]] = GoalSerializer(_goals, many=True).data

        response = auth_client.get(self.url + '?priority=4')

        assert response.status_code == 200
        assert response.json() == result

    def test_goal_list_with_priority__in(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_with_priority__in function is a test method. Accepts the following instances
        as arguments: authorized test client, User and Board. Performs the creation of test data.
        Makes a GET request to the URL '/goals/goal/list?priority__in=3,4' to output a list of Goal objects
        whose value of the 'priority' field is contained in the specified list. Checks the compliance
        of the status code and the content of the application response. If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        goals: List[Goal] = GoalFactory.create_batch(size=4, category=category)
        BoardParticipantFactory(board=board, user=user)
        goals[0].priority = Goal.Priority.low
        goals[0].save(update_fields=['priority'])
        goals[2].priority = Goal.Priority.high
        goals[2].save(update_fields=['priority'])
        goals[3].priority = Goal.Priority.critical
        goals[3].save(update_fields=['priority'])

        _goals = list()
        _goals.append(Goal.objects.get(id=goals[2].id))
        _goals.append((Goal.objects.get(id=goals[3].id)))
        result: List[Dict[str, Any]] = GoalSerializer(_goals, many=True).data
        result.sort(key=lambda x: x["title"])

        response = auth_client.get(self.url + '?priority__in=3,4')

        assert response.status_code == 200
        assert response.json() == result

    def test_goal_list_with_status(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_with_status function is a test method. Accepts the following instances as arguments:
        authorized test client, User and Board. Performs the creation of test data.
        Makes a GET request to the URL '/goals/goal/list?status=3' to output a list of Goal objects
        with the value of the 'status' field corresponding to the specified one. Checks the compliance
        of the status code and the content of the application response. If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        goals: List[Goal] = GoalFactory.create_batch(size=2, category=category)
        BoardParticipantFactory(board=board, user=user)
        goals[0].status = Goal.Status.done
        goals[0].save(update_fields=['status'])

        _goals: List[Goal] = [Goal.objects.get(id=goals[0].id)]
        result: List[Dict[str, Any]] = GoalSerializer(_goals, many=True).data

        response = auth_client.get(self.url + '?status=3')

        assert response.status_code == 200
        assert response.json() == result

    def test_goal_list_with_status__in(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_with_status__in function is a test method. Accepts the following instances
        as arguments: authorized test client, User and Board. Performs the creation of test data.
        Makes a GET request to the URL '/goals/goal/list?status__in=3,4' to output a list of Goal objects
        whose value of the 'status' field is contained in the specified list. Checks the compliance
        of the status code and the content of the application response. If there is a discrepancy, raises an exception.
        """
        category: GoalCategory = GoalCategoryFactory(board=board)
        goals: List[Goal] = GoalFactory.create_batch(size=4, category=category)
        BoardParticipantFactory(board=board, user=user)
        goals[1].status = Goal.Status.in_progress
        goals[1].save(update_fields=['status'])
        goals[2].status = Goal.Status.done
        goals[2].save(update_fields=['status'])
        goals[3].status = Goal.Status.archived
        goals[3].save(update_fields=['status'])

        _goals: list = list()
        _goals.append(Goal.objects.get(id=goals[2].id))
        _goals.append((Goal.objects.get(id=goals[3].id)))
        result: List[Dict[str, Any]] = GoalSerializer(_goals, many=True).data
        result.sort(key=lambda x: x["title"])

        response = auth_client.get(self.url + '?status__in=3,4')

        assert response.status_code == 200
        assert response.json() == result

    def test_goal_list_with_category(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_with_category function is a test method. Accepts the following instances as arguments:
        authorized test client, User and Board. Performs the creation of test data. Makes a GET request
        to the URL '/goals/goal/list?category=4' to output a list of Goal objects with the value
        of the 'category' field corresponding to the specified one. Checks the compliance of the status code
        and the content of the application response. If there is a discrepancy, raises an exception.
        """
        category1: GoalCategory = GoalCategoryFactory(board=board)
        category2: GoalCategory = GoalCategoryFactory(board=board)
        goals: list = list()
        goals.append(GoalFactory(category=category1))
        goals.append(GoalFactory(category=category2))
        BoardParticipantFactory(board=board, user=user)

        _goals: List[Goal] = [Goal.objects.get(id=goals[0].id)]
        result: List[Dict[str, Any]] = GoalSerializer(_goals, many=True).data

        response = auth_client.get(self.url + '?category=' + str(category1.id))

        assert response.status_code == 200
        assert response.json() == result

    def test_goal_list_with_category__in(self, auth_client, user: User, board: Board) -> None:
        """
        The test_goal_list_with_category__in function is a test method. Accepts the following instances
        as arguments: authorized test client, User and Board. Performs the creation of test data.
        Makes a GET request to the URL '/goals/goal/list?category__in=3,4' to output a list of Goal objects
        whose value of the 'category' field is contained in the specified list. Checks the compliance
        of the status code and the content of the application response. If there is a discrepancy, raises an exception.
        """
        categorys: List[GoalCategory] = GoalCategoryFactory.create_batch(size=4, board=board)
        goals: list = list()
        for category in categorys:
            goals.append(GoalFactory(category=category))
        BoardParticipantFactory(board=board, user=user)

        goals.pop(1)
        goals.pop(0)
        result: List[Dict[str, Any]] = GoalSerializer(goals, many=True).data
        result.sort(key=lambda x: x["title"])

        response = auth_client.get(self.url + '?category__in=' + str(categorys[2].id) + ',' + str(categorys[3].id))

        assert response.status_code == 200
        assert response.json() == result
