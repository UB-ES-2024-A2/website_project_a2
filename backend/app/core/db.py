""" Database configuration """
import mysql.connector

from app.models import UserCreate, BookCreate
from app.core.config import settings
from datetime import datetime

def get_db_connection():
    """ Creates a connection to the production database """
    return mysql.connector.connect(
        host=settings.HOST,
        user=settings.USERDB,
        password=settings.PASSWORD,
        database=settings.DATABASE,
        port=3306,
    )

def init_db(cursor) -> None:
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
    cursor.execute("SELECT id_user FROM users WHERE email = %s", (test_user.email,))
    userTest = cursor.fetchone()

    if not userTest:
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

    # Creating a BookCreate instance for testing
    testBook = BookCreate(
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
    cursor.execute("SELECT Title FROM Books WHERE title = %s", (testBook.title,))
    book = cursor.fetchone()

    if not book:
        # Insert a sample book into the database
        query_create_book = """
                        INSERT INTO Books (Title, Authors, Synopsis, BuyLink, Genres, Rating, Editorial, Comments, PublicationDate, Image)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
        cursor.execute(query_create_book, (
            testBook.title,
            testBook.authors,
            testBook.synopsis,
            testBook.buy_link,
            testBook.genres,
            testBook.rating,
            testBook.editorial,
            testBook.comments,
            testBook.publication_date,
            testBook.image
        ))

