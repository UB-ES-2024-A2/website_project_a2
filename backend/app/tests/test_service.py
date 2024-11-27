import pytest
from fastapi.testclient import TestClient

def test_not_found_page(client: TestClient) -> None:
    response = client.get("/not-found")
    assert response.status_code == 404 
    assert response.json() == {"detail": "Not Found"}  
