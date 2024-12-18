""" MyBooks related CRUD methods """
from app.models import MyBookCreate, MyBookOut, MyBooksOut
from typing import Any

def create_mybook(*, cursor, mybook_in: MyBookCreate) -> MyBookOut:
    """
    Creates a new entry in the 'mybooks' table and returns the details of the entry.

    Args:
        cursor: The database cursor to interact with the database.
        mybook_in (MyBookCreate): The details of the book to be added.

    Returns:
        MyBookOut: An object containing the details of the newly created entry.
    """
    query_create_mybook = """
        INSERT INTO mybooks (id_user, idBook)
        VALUES (%s, %s)
    """
    print(f"Attempting to insert: user_id={mybook_in.id_user}, book_id={mybook_in.id_book}")

    cursor.execute(query_create_mybook, (mybook_in.id_user, mybook_in.id_book))

    # Get the new entry ID
    new_mybook_id = cursor.lastrowid

    mybook_out = MyBookOut(
        id_entry=new_mybook_id,
        id_user=mybook_in.id_user,
        id_book=mybook_in.id_book
    )

    return mybook_out

def delete_user_book(*, cursor, id_user: int, id_book: int) -> bool:
    """
    Elimina la coincidencia entre un usuario y un libro en la tabla 'user_books'
    basándose en el ID del usuario y el ID del libro proporcionados.

    Args:
        cursor: El cursor de la base de datos para interactuar con la base de datos.
        id_user (int): El ID del usuario.
        idBook (int): El ID del libro.

    Returns:
        bool: True si la eliminación fue exitosa, de lo contrario False.
    """
    query_delete_user_book = """
        DELETE FROM mybooks
        WHERE id_user = %s AND idBook = %s
    """
    cursor.execute(query_delete_user_book, (id_user, id_book))

    # Verifica si se eliminó alguna fila (es decir, si se encontró y eliminó la coincidencia)
    return cursor.rowcount > 0

def get_mybooks(*, cursor, id_user: int) -> Any:
    """
    Obtiene los libros de un usuario basado en el ID del usuario y el ID del libro.

    Args:
        cursor: El cursor de la base de datos para interactuar con la base de datos.
        id_user (int): El ID del usuario.
        id_book (int): El ID del libro.

    Returns:
        MyBookOut: Un objeto con los detalles del libro si se encuentra, de lo contrario None.
    """
    query_get_mybook = """
        SELECT id_entry, id_user, idBook
        FROM mybooks
        WHERE id_user = %s
    """
    cursor.execute(query_get_mybook, (id_user,))

    # Recupera todos los resultados de la consulta
    result = cursor.fetchall()

    # Contar el total de libros
    count = len(result)

    if result:
        mybooks_out = [
            MyBookOut(
                id_entry=row[0],
                id_user=row[1],
                id_book=row[2]
            ) for row in result
        ]
        # Devolver la respuesta en el formato esperado
        return MyBooksOut(data=mybooks_out, count=count)
    else:
        return None
