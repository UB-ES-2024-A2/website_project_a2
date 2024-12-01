""" Tests configuration module """
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.db import init_db, get_db_connection

@pytest.fixture(scope="session", autouse=True)
def db() -> Generator:
    """
    Fixture to provide a database cursor for tests.
    Initializes the database with test data and cleans up afterward.
    """
    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    try:
        #Initialize the database with test data
        init_db(cursor)
        connection.commit()

        #Provide the cursor to the tests
        yield cursor

    finally:
        if connection.is_connected():
            # Clean up test data
            cursor.execute("DELETE FROM users WHERE email = 'test@test'")
            cursor.execute("DELETE FROM Books WHERE title = 'Test Book'")
            cursor.execute("DELETE FROM Books WHERE title = 'Test Book2'")
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

@pytest.fixture(scope="module")
def client() -> Generator:
    """
    Creates a FastAPI test client for the test.
    """
    with TestClient(app) as c:
        yield c
