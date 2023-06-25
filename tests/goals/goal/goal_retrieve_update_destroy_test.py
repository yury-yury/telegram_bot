import pytest

from goals.models import Goal


@pytest.mark.django_db
class TestGoalRetrieveUpdateDestroy:
    """
    The TestGoalRetrieveUpdateDestroy class combines all unit tests to check the functioning of the application
    when accessing the endpoint "/goals/goal/<pk>" using the pytest library.
    """
    url: str = '/goals/goal/'

    def test_goal_retrieve_get_without_authorization(self, client, goal: Goal) -> None:
        """
        The test_goal_retrieve_get_without_authorization function is a test method. Accepts the following test client
        and Goal instances as arguments. Makes a GET request to the URL '/goals/goal/<pk>' on behalf
        of a user who does not have authentication.. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        response = client.get(self.url + str(goal.id))

        assert response.status_code == 401
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_goal_update_put_without_authorization(self, client, goal: Goal) -> None:
        """
        The test_goal_update_put_without_authorization function is a test method. Accepts the following test client
        and Goal instances as arguments. Makes a PUT request to the URL '/goals/goal/<pk>' on behalf
        of a user who does not have authentication.. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        response = client.put(self.url + str(goal.id))

        assert response.status_code == 401
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_goal_update_patch_without_authorization(self, client, goal: Goal) -> None:
        """
        The test_goal_update_patch_without_authorization function is a test method. Accepts the following test client
        and Goal instances as arguments. Makes a PATCH request to the URL '/goals/goal/<pk>' on behalf
        of a user who does not have authentication.. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        response = client.patch(self.url + str(goal.id))

        assert response.status_code == 401
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_goal_delete_without_authorization(self, client, goal: Goal) -> None:
        """
        The test_goal_delete_without_authorization function is a test method. Accepts the following test client
        and Goal instances as arguments. Makes a DELETE request to the URL '/goals/goal/<pk>' on behalf of
        a user who does not have authentication.. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        response = client.delete(self.url + str(goal.id))

        assert response.status_code == 401
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}
