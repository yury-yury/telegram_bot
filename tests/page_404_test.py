def test_root_not_found(client) -> None:
    """
    The test_root_not_found function takes a test client as a parameter. It is intended for unit testing
    of the application when receiving a request at the address '/' using the pytest library.
    """
    response = client.get('/')
    assert response.status_code == 404
