""" Test CRUD operations on users """
from unittest.mock import MagicMock

from app.crud.rating import (
    create_rating, get_ratings, get_rating_by_id, delete_rating
)


def test_create_rating(db, second_book_id, user_id):
    """ Test for creating a new rating for a book."""
    comment = "Great book!"
    rating = 5

    # Llamar a la función que estás probando con el *mock* de cursor
    create_rating(cursor=db, id=second_book_id, user_id=user_id, comment=comment, rating=rating)

    row = get_ratings(cursor=db, book_id=second_book_id)

    assert row is not None
    assert row[0][3] == rating

def test_get_ratings(db, book_id):
    """ Test for retrieving all ratings and comments for a book."""
    ratings = get_ratings(cursor=db, book_id=book_id)

    assert ratings is not None
    assert len(ratings) > 0

def test_get_rating_by_id(db, second_book_id):
    """ Test for retrieving the book ID associated with a specific comment ID."""
    rate = get_rating_by_id(cursor=db, comment_id=second_book_id)

    assert rate is None

def test_delete_rating(db, comment_id):
    """ Test for deleting a specific rating by comment ID."""
    db = MagicMock()
    delete_rating(cursor=db, comment_id=comment_id)

    # Verify that the delete query was called correctly
    db.execute.assert_called_once_with(
        "DELETE FROM CommentRatingPerBook WHERE IdCommentRating = %s",
        (comment_id,)
    )