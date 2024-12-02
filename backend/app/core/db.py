""" Database configuration """
from datetime import datetime
import mysql.connector

from app.models import UserCreate, BookCreate
from app.core.config import settings

def get_db_connection():
    """ Creates a connection to the production database """
    return mysql.connector.connect(
        host=settings.HOST,
        user=settings.USERDB,
        password=settings.PASSWORD,
        database=settings.DATABASE,
        port=3306,
    )

def init_db(cursor):
    """ Initializes the database with a default superuser and a sample book """

    # Create a test user
    test_user = UserCreate(
        name="Test",
        surname="Test",
        username="test",
        email="test@test",
        password="test"
    )

    # Check if the test user exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (test_user.email,))
    existing_user = cursor.fetchone()

    if not existing_user:
        # Insert user test in the db
        query_create_user = """
            INSERT INTO users (name, surname, username, email, password)
            VALUES (%s, %s, %s, %s, %s)
            """
        cursor.execute(query_create_user, (
            test_user.name,
            test_user.surname,
            test_user.username,
            test_user.email,
            test_user.password
        ))

        user_id = cursor.lastrowid
    else:
        user_id = existing_user[0]

    # Creating a BookCreate instance for testing
    test_book = BookCreate(
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

    # Check if the test book exists
    cursor.execute("SELECT * FROM Books WHERE Title = %s", (test_book.title,))
    book = cursor.fetchone()

    if not book:
        # Insert a sample book into the database
        query_create_book = """
                        INSERT INTO Books (Title, Authors, Synopsis, BuyLink, Genres, Rating, Editorial, Comments, PublicationDate, Image)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
        cursor.execute(query_create_book, (
            test_book.title,
            test_book.authors,
            test_book.synopsis,
            test_book.buy_link,
            test_book.genres,
            test_book.rating,
            test_book.editorial,
            test_book.comments,
            test_book.publication_date,
            test_book.image
        ))

        book_id = cursor.lastrowid
    else:
        book_id = book[0]

    # Insert a sample rating into the database
    query_create_rating ="""
        INSERT INTO CommentRatingPerBook (IdUser, IdBook, Comment, Rating)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query_create_rating, (
        user_id,
        book_id,
        'Test Comment',
        1
    ))

    comment_id = cursor.lastrowid

    # Creating a BookCreate instance for testing without comments
    test_book.title = 'Test Book2'
    test_book.genres = 'Test Book2'

    # Check if the test book exists
    cursor.execute("SELECT * FROM Books WHERE Title = %s", (test_book.title,))
    book = cursor.fetchone()

    if not book:
        # Insert a sample book into the database
        query_create_book = """
                            INSERT INTO Books (Title, Authors, Synopsis, BuyLink, Genres, Rating, Editorial, Comments, PublicationDate, Image)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
        cursor.execute(query_create_book, (
            test_book.title,
            test_book.authors,
            test_book.synopsis,
            test_book.buy_link,
            test_book.genres,
            test_book.rating,
            test_book.editorial,
            test_book.comments,
            test_book.publication_date,
            test_book.image
        ))

        second_book_id = cursor.lastrowid
    else:
        second_book_id = book[0]

    return user_id, book_id, second_book_id, comment_id

