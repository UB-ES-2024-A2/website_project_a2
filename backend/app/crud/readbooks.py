from app.models import ReadBookCreate, ReadBookOut
from typing import Any

def create_readbook(*, cursor, readbook_in: ReadBookCreate) -> ReadBookOut:
    """
    Creates a new entry in the 'readbooks' table and returns the details of the entry.

    Args:
        cursor: The database cursor to interact with the database.
        readbook_in (ReadBookCreate): The details of the book to be added.

    Returns:
        ReadBookOut: An object containing the details of the newly created entry.
    """
    query_create_readbook = """
        INSERT INTO readbooks (id_user, idBook)
        VALUES (%s, %s)
    """
    print(f"Attempting to insert: user_id={readbook_in.id_user}, book_id={readbook_in.id_book}")

    cursor.execute(query_create_readbook, (readbook_in.id_user, readbook_in.id_book))

    # Get the new entry ID
    new_readbook_id = cursor.lastrowid

    readbook_out = ReadBookOut(
        id_entry=new_readbook_id,
        id_user=readbook_in.id_user,
        id_book=readbook_in.id_book
    )

    return readbook_out

def delete_user_readbook(*, cursor, id_user: int, id_book: int) -> bool:
    """
    Deletes the match between a user and a book in the 'readbooks' table
    based on the provided user ID and book ID.

    Args:
        cursor: The database cursor to interact with the database.
        id_user (int): The ID of the user.
        id_book (int): The ID of the book.

    Returns:
        bool: True if the deletion was successful, otherwise False.
    """
    query_delete_user_readbook = """
        DELETE FROM readbooks
        WHERE id_user = %s AND idBook = %s
    """
    cursor.execute(query_delete_user_readbook, (id_user, id_book))

    # Check if any rows were affected (i.e., the entry was found and deleted)
    return cursor.rowcount > 0

def get_readbook(*, cursor, id_user: int) -> Any:
    """
    Retrieves a book entry for a user based on the user ID and book ID.

    Args:
        cursor: The database cursor to interact with the database.
        id_user (int): The ID of the user.
        id_book (int): The ID of the book.

    Returns:
        ReadBookOut: An object with the details of the book if found, otherwise None.
    """
    query_get_readbook = """
        SELECT id_entry, id_user, idBook
        FROM readbooks
        WHERE id_user = %s
    """
    cursor.execute(query_get_readbook, (id_user, ))

    results = cursor.fetchall()
    if not results:
        return []
    readbooks_out = [
        ReadBookOut(
            id_entry=result[0],
            id_user=result[1],
            id_book=result[2]
        )
        for result in results
    ]
    return readbooks_out
def check_readbook_exists(*, cursor, readbook_in: ReadBookCreate) -> bool:
    """
    Checks if a book entry already exists for a given user in the 'readbooks' table.
    
    Args:
        cursor: The database cursor to interact with the database.
        readbook_in (ReadBookCreate): The details of the book to check.
    
    Returns:
        bool: True if the book entry exists, False otherwise.
    """
    query_check_readbook = """
        SELECT COUNT(*) 
        FROM readbooks 
        WHERE id_user = %s AND idBook = %s
    """
    
    cursor.execute(query_check_readbook, (readbook_in.id_user, readbook_in.id_book))
    (count,) = cursor.fetchone()
    return count > 0
