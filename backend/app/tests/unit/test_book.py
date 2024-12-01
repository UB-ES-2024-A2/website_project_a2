""" Tests CRUD operations on books """
from datetime import datetime
from unittest.mock import MagicMock

from app.models import BookCreate

from app.crud.book import (
    get_book_by_id, get_book_by_title,
    get_books_by_genres, get_all_books,
    create_book, get_books_by_key, update_book, delete_book
)

def test_create_book(db):
    """ Test creating a book """
    db = MagicMock()

    book_in = BookCreate(
        title="Test Book",
        authors="Test Book",
        synopsis="Test Book",
        buy_link="Test Book",
        genres="Test Book",
        rating=0.0,
        editorial="Test Book",
        comments="Test Book",
        publication_date=datetime.now().isoformat(),
        image="test"
    )

    book = create_book(cursor=db, book_in=book_in)

    # Verify that the insert query was called correctly
    db.execute.assert_called_once_with(
        """
        INSERT INTO Books (Title, Authors, Synopsis, BuyLink, Genres, Rating, Editorial, Comments, PublicationDate, Image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
        (
            book_in.title,
            book_in.authors,
            book_in.synopsis,
            book_in.buy_link,
            book_in.genres,
            book_in.rating,
            book_in.editorial,
            book_in.comments,
            book_in.publication_date,
            book_in.image
        )
    )


def test_get_book_by_id(db, book_id):
    """ Test for retrieving a book by ID."""
    book = get_book_by_id(cursor=db, book_id=book_id)

    assert book is not None
    assert book.id_book == book_id

def test_get_book_by_title(db):
    """ Test for retrieving a book by title."""
    title = 'Test Book'
    book = get_book_by_title(cursor=db, book_title=title)

    assert book is not None
    assert book[1] == title

def test_get_books_by_genres(db):
    """ Test for retrieving books by genres."""
    books = get_books_by_genres(cursor=db, genres=["Test Book"])

    assert books is not None
    assert books.count > 0

def test_get_all_books(db):
    """ Test for retrieving all books."""
    books = get_all_books(cursor=db)

    assert books is not None
    assert len(books.data) > 0

def test_get_books_by_key(db):
    """ Test for retrieving books by key."""
    books = get_books_by_key(cursor=db, keyword="Test")

    assert books is not None
    assert books.count > 0

def test_update_book(db, book_id):
    """ Test updating a book."""
    book_in = BookCreate(
        title="Test Book",
        authors="Test Book",
        synopsis="Test Book",
        buy_link="Test Book",
        genres="Test Book",
        rating=0.0,
        editorial="Test Book",
        comments="Test Book",
        publication_date=datetime.now().isoformat(),
        image="test"
    )
    db = MagicMock()

    update_book(cursor=db, book_id=book_id, book_in=book_in)

    # Verify that the insert query was called correctly
    db.execute.assert_called_once_with( """
                UPDATE Books SET Title = %s, Authors = %s, Synopsis = %s, BuyLink = %s, Genres = %s, Rating = %s,
                Editorial = %s, Comments = %s, PublicationDate = %s, Image = %s
                WHERE IdBook = %s
            """,
       (
           book_in.title,
           book_in.authors,
           book_in.synopsis,
           book_in.buy_link,
           book_in.genres,
           book_in.rating,
           book_in.editorial,
           book_in.comments,
           book_in.publication_date,
           book_in.image,
           book_id
       ))

def test_delete_book(db, book_id):
    db = MagicMock()

    delete_book(cursor=db, book_id=book_id)

    # Verify that the insert query was called correctly
    db.execute.assert_called_once_with("DELETE FROM Books WHERE IdBook = %s",
                                       (book_id,))
