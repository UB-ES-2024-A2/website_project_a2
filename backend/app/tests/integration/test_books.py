""" Test suite for book-related endpoints """
from fastapi.testclient import TestClient

def test_get_ratings_per_user(client: TestClient):
    """
    Test case for reading user ratings

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The response body contains a "data" key with a list of books.
        - The response contains a "count" key with the total number of books.
    """
    id_user = 9
    response = client.get(f"/api/v1/books/books/ratings/{id_user}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()

    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_readbooks(client: TestClient, db):
    """
    Test case for getting
    Args:
        client (TestClient): The TestClient instance to send requests to the API.
    Asserts:
        - The response status code is 200.
        - The response body contains a "data" key with a list of books.
        - The response contains a "count" key with the total number of books.
    """
    id_user = 22
    id_book = 3
    response = client.get(f"/api/v1/readbooks/readbooks/{id_user}/{id_book}")
    assert response.status_code == 200

    data = response.json()

    print(data)

    assert "id_user" in data
    assert "id_book" in data
    assert "id_entry" in data


def test_get_mybooks(client: TestClient, db):
    """
    Test case for getting
    Args:
        client (TestClient): The TestClient instance to send requests to the API.
    Asserts:
        - The response status code is 200.
        - The response body contains a "data" key with a list of books.
        - The response contains a "count" key with the total number of books.
    """
    id_user = 24
    response = client.get(f"/api/v1/mybooks/{id_user}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()

    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) <= 20

    for book in data["data"]:
        assert "id_book" in book
        assert "title" in book
        assert "authors" in book
        assert "synopsis" in book
        assert "buy_link" in book
        assert "genres" in book
        assert "rating" in book
        assert "editorial" in book
        assert "comments" in book
        assert "publication_date" in book
        assert "image" in book

    assert "count" in data
    assert isinstance(data["count"], int)


def test_read_top5_matched_books(client: TestClient, db) -> None:
    """
    Test case for reading top 5 matched books based on a search keyword.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The response body contains a "data" key with a list of books.
        - The response contains a "count" key with the total number of books.
    """
    keyword = "Test Boo"
    response = client.get(f"/api/v1/books/{keyword}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()

    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) <= 5

    for book in data["data"]:
        assert "id_book" in book
        assert "title" in book
        assert "authors" in book
        assert "synopsis" in book
        assert "buy_link" in book
        assert "genres" in book
        assert "rating" in book
        assert "editorial" in book
        assert "comments" in book
        assert "publication_date" in book
        assert "image" in book

    assert "count" in data
    assert isinstance(data["count"], int)

def test_filter_books_by_genres(client: TestClient, db) -> None:
    """
    Test case for filtering books by genres.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The response body contains "data" and "count" keys.
        - Each book contains the necessary fields.
    """
    genres = ["Test Book"]

    response = client.post("/api/v1/books/filter-by-genres", json=genres)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()
    assert "data" in data
    assert "count" in data

    assert isinstance(data["data"], list)

    for book in data["data"]:
        assert "id_book" in book
        assert "title" in book
        assert "authors" in book
        assert "synopsis" in book
        assert "buy_link" in book
        assert "genres" in book
        assert "rating" in book
        assert "editorial" in book
        assert "comments" in book
        assert "publication_date" in book
        assert "image" in book

    assert isinstance(data["count"], int)
    assert data["count"] >= len(data["data"])


def test_get_book_by_id(client: TestClient, db, book_id) -> None:
    """
    Test case for getting a book by its ID.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The returned book matches the searched book.
    """
    # Get the book by id
    response = client.get(f"api/v1/books/book/{book_id}")
    book = response.json()

    assert response.status_code == 200
    assert book
    assert "id_book" in book
    assert book['id_book'] == book_id

def test_get_book_by_not_found_id(client: TestClient, db) -> None:
    """
    Test case for getting a book by a non-existent ID.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 404.
        - The response message is "Book not found with the provided id".
    """
    # Get the book by id
    response = client.get(f"api/v1/books/book/{-9}")
    book = response.json()

    assert response.status_code == 404
    assert book["detail"] == "Book not found with the provided id"

def test_get_book_by_not_id(client: TestClient, db) -> None:
    """
    Test case for getting a book by a non-existent ID.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 404.
        - The response contains an error message for the book not found.
    """
    # Get the book by id
    response = client.get("api/v1/books/book/h")
    book = response.json()

    assert response.status_code == 422
    assert book["detail"][0]['msg'] == ('Input should be a valid integer, '
                                        'unable to parse string as an integer')

def test_get_books(client: TestClient, db) -> None:
    """
    Test case for getting all books.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The returned data contains a list of books with more than 0 items.
    """
    # Get all books
    response = client.get("/api/v1/books")

    assert response.status_code == 200
    books = response.json()['data']
    assert len(books) > 0

def test_get_two_books(client: TestClient, db) -> None:
    """
    Test case for getting a limited number of books.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The returned data contains exactly 2 books.
    """
    # Get first two books
    response = client.get("/api/v1/books/?skip=0&limit=2")

    assert response.status_code == 200
    books = response.json()['data']
    assert len(books) == 2