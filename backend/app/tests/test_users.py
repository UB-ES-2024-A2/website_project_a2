""" Test suite for user-related endpoints """
from fastapi.testclient import TestClient

def test_read_top5_matched_users(client: TestClient, db) -> None:
    """
    Test case for reading the top 5 matched users based on a search keyword.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The response body contains a "data" key with a list of users.
        - Each user in the list contains expected fields (id_user, name, surname, username, email).
    """
    keyword = "Test"
    response = client.get(f"/api/v1/users/{keyword}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()

    assert "data" in data
    assert isinstance(data["data"], list)

    if len(data["data"]) > 0:
        user = data["data"][0]
        assert "id_user" in user
        assert "name" in user
        assert "surname" in user
        assert "username" in user
        assert "email" in user

def test_read_users(client: TestClient, db) -> None:
    """
    Test case for reading users with pagination support.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The response body contains a "data" key with a list of users.
        - The response includes a "count" key representing the total number of users.
        - The list of users is limited by the "limit" parameter.
    """
    skip = 0
    limit = 10

    response = client.get(f"/api/v1/users/?skip={skip}&limit={limit}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()

    assert "data" in data
    assert isinstance(data["data"], list)
    assert isinstance(data["count"], int)
    assert len(data["data"]) <= limit

    if len(data["data"]) > 0:
        user = data["data"][0]
        assert "id_user" in user
        assert "name" in user
        assert "surname" in user
        assert "username" in user
        assert "email" in user
