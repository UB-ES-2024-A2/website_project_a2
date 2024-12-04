""" Test suite for service-related endpoints """
from fastapi.testclient import TestClient

def test_not_found_page(client: TestClient) -> None:
    """
    Test case for the "not found" page.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        The response status code is 404.
        The response body contains a "detail" key with the value "Not Found".
    """
    response = client.get("/not-found")

    assert response.status_code == 404

    assert response.json() == {"detail": "Not Found"}
