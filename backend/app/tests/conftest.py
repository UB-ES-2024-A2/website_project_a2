""" Tests configuration module """
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.db import init_db, get_db_connection

@pytest.fixture(scope="session", autouse=True)
def db(request) -> Generator:
    """
    Fixture to provide a database cursor for tests.
    Initializes the database with test data and cleans up afterward.
    """
    connection = get_db_connection()

    cursor = connection.cursor()

    # Initialize pre-test sets to avoid UnboundLocalError
    pre_test_user_ids = set()
    pre_test_book_ids = set()

    try:
        # Capture pre-test IDs
        cursor.execute("SELECT id_user FROM users")
        pre_test_user_ids = {row[0] for row in cursor.fetchall()}

        cursor.execute("SELECT IdBook FROM Books")
        pre_test_book_ids = {row[0] for row in cursor.fetchall()}

        # Initialize the database with test data
        user_id, book_id, second_book_id, comment_id = init_db(cursor)
        connection.commit()

        # Store user_id in the request object to be accessed by other fixtures
        request.node.user_id = user_id
        request.node.book_id = book_id
        request.node.second_book_id = second_book_id
        request.node.comment_id = comment_id

        # Provide the cursor to the tests

        yield cursor

    finally:
        if connection.is_connected():

            # Find and delete users created during tests
            cursor.execute("SELECT id_user FROM users")
            post_test_user_ids = {row[0] for row in cursor.fetchall()}
            new_user_ids = filter(lambda id_user: id_user not in pre_test_user_ids, post_test_user_ids)
            new_user_ids = list(new_user_ids)


            if new_user_ids and len(new_user_ids) < len(pre_test_user_ids):
                cursor.executemany(
                    "DELETE FROM users WHERE id_user = %s", [(user_id,) for user_id in new_user_ids]
                )

            # Find and delete books created during tests
            cursor.execute("SELECT IdBook FROM Books")
            post_test_book_ids = {row[0] for row in cursor.fetchall()}
            new_book_ids = filter(lambda IdBook: IdBook not in pre_test_book_ids, post_test_book_ids)
            new_book_ids = list(new_book_ids)


            if new_book_ids and len(new_book_ids) < len(pre_test_book_ids):
                cursor.executemany(
                   "DELETE FROM Books WHERE IdBook = %s", [(book_id,) for book_id in new_book_ids]
                )

            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

@pytest.fixture(scope="session")
def user_id(request) -> int:
    """
    Fixture to provide the user_id from the db fixture.
    """
    return getattr(request.node, "user_id", None)

@pytest.fixture(scope="session")
def book_id(request) -> int:
    """
    Fixture to provide the book_id from the db fixture.
    """
    return getattr(request.node, "book_id", None)

@pytest.fixture(scope="session")
def second_book_id(request) -> int:
    """
    Fixture to provide the second_book_id from the db fixture.
    """
    return getattr(request.node, "second_book_id", None)

@pytest.fixture(scope="session")
def comment_id(request) -> int:
    """
    Fixture to provide the comment_id from the db fixture.
    """
    return getattr(request.node, "comment_id", None)

@pytest.fixture(scope="module")
def client() -> Generator:
    """
    Creates a FastAPI test client for the test.
    """
    with TestClient(app) as c:
        yield c
