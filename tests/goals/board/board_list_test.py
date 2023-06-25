import pytest


@pytest.mark.django_db
class TestBoardList:
    """
    The TestBoardList class combines all unit tests to check the functioning of the application when accessing
    the endpoint "/goals/board/list" using the pytest library.
    """
    url: str = '/goals/board/list'

    def test_board_list_without_authorization(self, client) -> None:
        """
        The test_board_list_without_authorization function is a test method. Takes as an argument an instance
        of the test client. Makes a GET request to the URL '/goals/board/list' on behalf of a user
        who does not have authentication. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        response = client.get(self.url)

        assert response.status_code == 401
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}
