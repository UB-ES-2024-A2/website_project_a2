""" Test suite for comment-related endpoints """
from fastapi.testclient import TestClient

def test_get_rating(client: TestClient, db, book_id) -> None:
    """
    Test case for getting the rating and comments of a book.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The response contains the username, comment, and rating.
    """
    # Get the rating
    response = client.get(f"api/v1/books/CommentRatingPerBook/{book_id}")

    assert response.status_code == 200
    rating = response.json()['comments'][0]
    assert rating["username"] == "test"
    assert rating['comment'] == "Test Comment"
    assert rating['rating'] == 1

def test_get_rating_not_found_book(client: TestClient, db) -> None:
    """
    Test case for getting ratings of a book that doesn't exist.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 404.
        - The response message is "Book not found".
    """
    # Get the book id
    book_id = -1

    # Get the rating
    response = client.get(f"api/v1/books/CommentRatingPerBook/{book_id}")

    assert response.status_code == 404
    message = response.json()
    assert message["detail"] == "Book not found."

def test_get_rating_book_without_ratin(client: TestClient, db, second_book_id) -> None:
    """
    Test case for getting ratings of a book without any ratings or comments.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The response message is "No comments or ratings found for this book".
    """
    # Get the rating
    response = client.get(f"api/v1/books/CommentRatingPerBook/{second_book_id}")

    assert response.status_code == 200
    message = response.json()
    assert message["message"] == "No comments or ratings found for this book."

def test_get_rating_invalid_id(client: TestClient, db) -> None:
    """
    Test case for getting ratings with an invalid book ID.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 422.
        - The error message indicates that the ID is invalid and cannot be parsed.
    """
    # Get the rating
    response = client.get("api/v1/books/CommentRatingPerBook/h")

    assert response.status_code == 422
    message = response.json()
    assert message["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'


def test_post_book_rating(client: TestClient, db, book_id, user_id) -> None:
    """
    Test case for posting a comment and rating for a book.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The response confirms the comment and rating have been added.
    """
    # Post rating
    response = client.post(
        f'/api/v1/books/books/{book_id}/comments',
        params={
            "user_id": user_id,
            "comment": "test",
            "rating": 5,
        })

    assert response.status_code == 200
    message = response.json()
    assert message['message'] == "Comment and rating successfully added."

def test_post_book_rating_not_found_book(client: TestClient, db, user_id) -> None:
    """
    Test case for posting a book rating when the book is not found.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 404.
        - The response message is "Book not found".
    """
    # Get the book id
    book_id = -1

    # Post rating
    response = client.post(
        f'/api/v1/books/books/{book_id}/comments',
        params={
            "user_id": user_id,
            "comment": "test",
            "rating": 5,
        })

    assert response.status_code == 404
    message = response.json()
    assert message["detail"] == "Book not found."

def test_post_book_rating_not_found_user(client: TestClient, db, book_id) -> None:
    """
    Test case for posting a book rating when the user is not found.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 404.
        - The response message is "User not found".
    """
    # Get the user id
    user_id = -1

    # Post rating
    response = client.post(
        f'/api/v1/books/books/{book_id}/comments',
        params={
            "user_id": user_id,
            "comment": "test",
            "rating": 5,
        })

    assert response.status_code == 404
    message = response.json()
    assert message['detail'] == "User not found."

def test_post_book_rating_not_valid_rating(client: TestClient, db, book_id, user_id) -> None:
    """
    Test case for posting a book rating with an invalid rating value.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 400.
        - The response message indicates that the rating must be between 1 and 5.
    """
    # Get the rating
    rating = -1

    # Post rating
    response = client.post(
        f'/api/v1/books/books/{book_id}/comments',
        params={
            "user_id": user_id,
            "comment": "test",
            "rating": rating,
        })

    assert response.status_code == 400
    message = response.json()
    assert message['detail'] == "Rating must be between 1 and 5."

def test_post_book_rating_not_param(client: TestClient, db, book_id) -> None:
    """
    Test case for posting a book rating without the required parameters.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 422.
        - The response message indicates that a field is required.
    """
    # Post rating
    response = client.post(
        f'/api/v1/books/books/{book_id}/comments')

    print('response', response)
    print('message', response.json())

    assert response.status_code == 422
    message = response.json()
    assert message['detail'][0]['msg'] == 'Field required'

def test_delete_book_rating(client: TestClient, db, book_id) -> None:
    """
    Test case for deleting a book rating.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 200.
        - The message confirms that the comment was successfully deleted.
    """
    # Get the rating id
    ratings = client.get(f"api/v1/books/CommentRatingPerBook/{book_id}")
    rating_id = ratings.json()['comments'][0]['id_comment_rating']

    # Delete comment
    response = client.delete(f"api/v1/books/CommentRatingPerBook/{rating_id}")
    message = response.json()

    assert response.status_code == 200
    assert message['message'] == "Comment successfully deleted."

def test_delete_book_rating_not_found_rating(client: TestClient, db) -> None:
    """
    Test case for attempting to delete a non-existent book rating.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 404.
        - The message confirms that the comment was not found.
    """
    # Get the rating id
    rating_id = -1

    # Delete comment
    response = client.delete(f"api/v1/books/CommentRatingPerBook/{rating_id}")

    assert response.status_code == 404
    message = response.json()
    assert message["detail"] == "Comment not found."

def test_delete_book_rating_not_valid_id(client: TestClient, db) -> None:
    """
    Test case for attempting to delete a book rating with an invalid ID.

    Args:
        client (TestClient): The TestClient instance to send requests to the API.

    Asserts:
        - The response status code is 422.
        - The message confirms that the ID is invalid.
    """
    # Delete comment
    response = client.delete("api/v1/books/CommentRatingPerBook/{h}")

    assert response.status_code == 422
    message = response.json()
    assert message["detail"][0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'

