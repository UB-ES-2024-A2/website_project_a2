from fastapi.testclient import TestClient

def test_read_top5_matched_books(client: TestClient, db) -> None:
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


def test_get_book_by_id(client: TestClient, db) -> None:
    # Get the book id
    book_searched = client.post("/api/v1/books/filter-by-genres", json=["Test Book"]).json()["data"][0]
    book_id = book_searched['id_book']

    # Get the book by id
    response = client.get(f"api/v1/books/book/{book_id}")
    book = response.json()

    assert response.status_code == 200
    assert book
    assert "title" in book
    assert book['title'] == book_searched['title']
    assert "authors" in book
    assert book['authors'] == book_searched['authors']
    assert "synopsis" in book
    assert book['synopsis'] == book_searched['synopsis']
    assert "buy_link" in book
    assert book['buy_link'] == book_searched['buy_link']
    assert "genres" in book
    assert book['genres'] == book_searched['genres']
    assert "rating" in book
    assert book['rating'] == book_searched['rating']
    assert "editorial" in book
    assert book['editorial'] == book_searched['editorial']
    assert "comments" in book
    assert book['comments'] == book_searched['comments']
    assert "publication_date" in book
    assert book['publication_date'] == book_searched['publication_date']
    assert "image" in book
    assert book['image'] == book_searched['image']

def test_get_book_by_not_found_id(client: TestClient, db) -> None:
    # Get the book by id
    response = client.get(f"api/v1/books/book/{-9}")
    book = response.json()

    assert response.status_code == 404
    assert book["detail"] == "Book not found with the provided id"

def test_get_book_by_not_id(client: TestClient, db) -> None:
    # Get the book by id
    response = client.get("api/v1/books/book/h")
    book = response.json()

    assert response.status_code == 422
    assert book["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

def test_delete_book_rating(client: TestClient, db) -> None:
    # Get the book id
    book_searched = client.post("/api/v1/books/filter-by-genres", json=["Test Book"]).json()["data"][0]
    book_id = book_searched['id_book']

    # Get the rating id
    ratings = client.get(f"api/v1/books/CommentRatingPerBook/{book_id}")
    rating_id = ratings.json()['comments'][0]['id_comment_rating']

    # Delete comment
    response = client.delete(f"api/v1/books/CommentRatingPerBook/{rating_id}")
    message = response.json()

    assert response.status_code == 200
    assert message['message'] == "Comment successfully deleted."

def test_delete_book_rating_not_found_rating(client: TestClient, db) -> None:
    # Get the rating id
    rating_id = -1

    # Delete comment
    response = client.delete(f"api/v1/books/CommentRatingPerBook/{rating_id}")

    assert response.status_code == 404
    message = response.json()
    assert message["detail"] == "Comment not found."

def test_delete_book_rating_not_valid_id(client: TestClient, db) -> None:
    # Delete comment
    response = client.delete("api/v1/books/CommentRatingPerBook/{h}")

    assert response.status_code == 422
    message = response.json()
    assert message["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'
