""" Book related CRUD methods """
from typing import Any
from datetime import datetime
from app.models import BookCreate, BookOut, BooksOut, BookUpdate, Book

def create_book(*, cursor, book_in: BookCreate) -> BookOut:
    """
    Creates a new book entry in the database and returns the created book's details.

    Args:
        session (SessionDep): The database session used to interact with the database.
        book_in (BookCreate): An object containing the information for the book to be created.

    Returns:
        BookOut: An object containing the details of the newly created book, including its generated ID.
    """
    book = Book.model_validate(book_in)

    # Insert book to the db
    query_create_book = """
        INSERT INTO Books (Title, Authors, Synopsis, BuyLink, Genres, Rating, Editorial, Comments, PublicationDate, Image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query_create_book, (
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
    ))

    # Get the book ID
    new_book_id = cursor.lastrowid

    # Prepare the publication date, converting if necessary
    if isinstance(book_in.publication_date, datetime):
        publication_date = book_in.publication_date.isoformat()
    elif isinstance(book_in.publication_date, str):
        # Ensure the publication date is a valid string if passed directly
        publication_date = book_in.publication_date
    else:
        publication_date = None  # If it's None or any other type, set to None

    # Create Book out object
    book_out = BookOut(
        id_book=new_book_id,
        title=book_in.title,
        authors=book_in.authors,
        synopsis=book_in.synopsis,
        buy_link=book_in.buy_link,
        genres=book_in.genres,
        rating=book_in.rating,
        editorial=book_in.editorial,
        comments=book_in.comments,
        publication_date=publication_date,
        image=book_in.image
    )

    return book_out

def get_book_by_id(*, cursor, book_id: int) -> Any:
    """
    Retrieves a book from the database by its ID and returns its details.

    Args:
        session (SessionDep): The database session used to interact with the database.
        book_id (int): The ID of the book to be retrieved.

    Returns:
        BookOut: An object containing the details of the book if found, or None if the book is not found.
    """
    # Consulta para obtener un libro por su ID
    query_book = """
                SELECT IdBook as id_book, Title as title, Authors as authors, Synopsis as synopsis, BuyLink as buy_link, 
                Genres as genres, Rating as rating, Editorial as editorial, Comments as comments, PublicationDate as publication_date, Image as image from Books
                WHERE IdBook = %s
            """
    cursor.execute(query_book, (book_id,))
    row = cursor.fetchone()

    if not row:
        return None

    # Transformar la fila obtenida en un objeto BookOut
    book_out = BookOut(
        id_book=row[0],
        title=row[1],
        authors=row[2],
        synopsis=row[3],
        buy_link=row[4],
        genres=row[5],
        rating=row[6],
        editorial=row[7],
        comments=row[8],
        publication_date=row[9].isoformat() if row[9] else None,  # Convertir a string
        image=row[10]
    )

    return book_out

def get_book_by_title(*, cursor, book_title: str) -> Any:
    """
    Retrieves a book from the database by its title.

    Args:
        session (SessionDep): The database session used to interact with the database.
        book_title (str): The title of the book to be retrieved.

    Returns:
        Any: The title of the book if found, or None if the book does not exist.
    """

    # Verificar si el libro ya existe por título
    query_check_book = "SELECT * FROM Books WHERE title = %s"
    cursor.execute(query_check_book, (book_title,))
    existing_book = cursor.fetchone()

    if not existing_book:
        return None

    return existing_book

def get_books_by_genres(*, cursor, genres: list[str]) -> BookOut:
    """
    Retrieves a list of books from the database that match the specified genres.

    Args:
        session (SessionDep): The database session object used to execute the queries.
        genres (list[str]): A list of genre names to filter the books by.

    Returns:
        BooksOut: A data structure containing a list of `BookOut` objects and the total count of matching books.

    Raises:
        Exception: Potentially raises an exception if there is an error with the database query or connection.

    Notes:
        - The function dynamically generates a SQL query to filter books based on the provided genres.
        - The results are returned in the form of `BooksOut`, which includes the books and a total count.
    """

    # Crear la consulta dinámica para los géneros
    query_books = f"""
                SELECT IdBook as id_book, Title as title, Authors as authors, Synopsis as synopsis, BuyLink as buy_link, 
                Genres as genres, Rating as rating, Editorial as editorial, Comments as comments, PublicationDate as publication_date, Image as image
                FROM Books
                WHERE Genres IN ({', '.join(['%s'] * len(genres))})
            """

    # Ejecutar la consulta con los géneros proporcionados
    cursor.execute(query_books, tuple(genres))
    filas = cursor.fetchall()

    # Contar el total de libros
    query_count = "SELECT COUNT(1) FROM Books WHERE Genres IN ({})".format(', '.join(['%s'] * len(genres)))
    cursor.execute(query_count, tuple(genres))
    count = cursor.fetchone()[0]

    # Transformar las filas obtenidas en una lista de objetos BookOut
    books_data = [
        BookOut(
            id_book=row[0],
            title=row[1],
            authors=row[2],
            synopsis=row[3],
            buy_link=row[4],
            genres=row[5],
            rating=row[6],
            editorial=row[7],
            comments=row[8],
            publication_date=row[9].isoformat() if row[9] else None,  # Convertir a string
            image=row[10]
        ) for row in filas
    ]

    return BooksOut(data=books_data, count=count)

def get_books_by_key(*, cursor, keyword: str) -> BookOut:
    """
    Retrieves a list of books from the database that match a given keyword in their title or authors.

    Args:
        cursor: The database cursor object used to execute the queries.
        keyword (str): The keyword to search for in the book titles and authors.

    Returns:
        BooksOut: A data structure containing a list of `BookOut` objects and the total count of all books.
    """
    # Crear la consulta de búsqueda
    query = """
                   SELECT IdBook, Title, Authors, Synopsis, BuyLink, Genres, Rating, Editorial, Comments, PublicationDate, Image
                   FROM Books
                   WHERE Title LIKE %s OR Authors LIKE %s
                   ORDER BY Rating DESC
                   LIMIT 5
               """

    # Preparar el parámetro de búsqueda con el carácter comodín
    search_param = f"%{keyword}%"

    # Ejecutar la consulta
    cursor.execute(query, (search_param, search_param))

    # Obtener los resultados
    resultados = cursor.fetchall()

    # Contar el total de libros
    query_count = "SELECT COUNT(1) FROM Books"
    cursor.execute(query_count)
    count = cursor.fetchone()[0]

    books_data = [
        BookOut(
            id_book=row[0],
            title=row[1],
            authors=row[2],
            synopsis=row[3],
            buy_link=row[4],
            genres=row[5],
            rating=row[6],
            editorial=row[7],
            comments=row[8],
            publication_date=row[9].isoformat() if row[9] else None,  # Convertir a string
            image=row[10]
        ) for row in resultados
    ]

    return BooksOut(data=books_data, count=count)

def get_all_books(*, cursor, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieves all books from the database with pagination support.

    Args:
        session (SessionDep): The database session used for database interactions.
        skip (int, optional): The number of books to skip for pagination (default is 0).
        limit (int, optional): The maximum number of books to retrieve (default is 100).

    Returns:
        Any: An object containing the list of books and the total count of books in the database.
    """

    # Consulta para obtener los libros con paginación
    query_books = """
                SELECT IdBook as id_book, Title as title, Authors as authors, Synopsis as synopsis, BuyLink as buy_link, 
                Genres as genres, Rating as rating, Editorial as editorial, Comments as comments, PublicationDate as publication_date, Image as image from Books
                LIMIT %s OFFSET %s;
            """
    cursor.execute(query_books, (limit, skip))
    # cursor.execute(query_books)
    filas = cursor.fetchall()

    # Contar el total de libros
    query_count = "SELECT COUNT(1) FROM Books"
    cursor.execute(query_count)
    count = cursor.fetchone()[0]
    # Transformar las filas obtenidas en una lista de objetos BookOut
    books_data = [
        BookOut(
            id_book=row[0],
            title=row[1],
            authors=row[2],
            synopsis=row[3],
            buy_link=row[4],
            genres=row[5],
            rating=row[6],
            editorial=row[7],
            comments=row[8],
            publication_date=row[9].isoformat() if row[9] else None,  # Convertir a string
            image=row[10]
        ) for row in filas
    ]

    return BooksOut(data=books_data, count=count)

def update_book(*, cursor, book_id: int, book_in: BookUpdate) -> BookOut:
    """
    Updates a book in the database using the values provided in book_in.

    Args:
        session (SessionDep): The database session to perform the operation.
        book_id (int): The ID of the book to be updated.
        book_in (BookUpdate): An object containing the updated book data.

    Returns:
        BookOut: An object with the details of the updated book.
    """

    # Actualizar el libro
    query_update_book = """
                UPDATE Books SET Title = %s, Authors = %s, Synopsis = %s, BuyLink = %s, Genres = %s, Rating = %s,
                Editorial = %s, Comments = %s, PublicationDate = %s, Image = %s
                WHERE IdBook = %s
            """
    cursor.execute(query_update_book, (
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

    # Transformar la fila obtenida en un objeto BookOut
    book_out = BookOut(
        id_book=book_id,
        title= book_in.title,
        authors=book_in.authors,
        synopsis=book_in.synopsis,
        buy_link=book_in.buy_link,
        genres=book_in.genres,
        rating=book_in.rating,
        editorial=book_in.editorial,
        comments=book_in.comments,
        publication_date=book_in.publication_date,
        image=book_in.image
    )

    return book_out

def delete_book(*, cursor, book_id: int) -> None:
    """
    Deletes a book record from the database by its unique book ID.

    Args:
        session (SessionDep): The database session object used to interact with the database.
        book_id (int): The unique identifier of the book to be deleted.

    Returns:
        None: This function does not return any value. It only performs the deletion and commits the transaction.

    Raises:
        Exception: An exception may be raised if there are any database errors or if the book ID does not exist.
    """

    # Eliminar el libro
    query_delete_book = "DELETE FROM Books WHERE IdBook = %s"
    cursor.execute(query_delete_book, (book_id,))

def update_avg(*, cursor, id_book,  avg_rating) -> None:
    """
    Updates the average rating of a book in the database.

    Args:
        cursor (cursor): The database cursor for executing the SQL query.
        id_book (int): The ID of the book whose rating needs to be updated.
        avg_rating (float): The new average rating to be set for the book.

    Returns:
        None
    """
    query_update_book = "UPDATE Books SET Rating = %s WHERE IdBook = %s"
    cursor.execute(query_update_book, (avg_rating, id_book))
