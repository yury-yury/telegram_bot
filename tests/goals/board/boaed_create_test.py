import pytest


@pytest.mark.django_db
class TestBoardCreate:
    """
    The TestBoardCreate class combines all unit tests to check the functioning of the application when accessing
    the endpoint "/goals/board/create" using the pytest library.
    """
    url: str = '/goals/board/create'

    def test_board_create_without_authorization(self, client) -> None:
        """
        The test_board_create_without_authorization function is a test method. Takes as an argument an instance
        of the test client. Makes a POST request to the URL '/goals/board/create' on behalf of a user
        who does not have authentication. Checks the compliance of the status code and the content
        of the application response. If there is a discrepancy, raises an exception.
        """
        response = client.post(self.url)

        assert response.status_code == 401
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}
