from typing import Any
from fastapi import APIRouter, Depends, HTTPException
import mysql.connector

from app.core.config import settings
from app.models import Book, BookCreate, BookOut, BooksOut, BookUpdate

from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings

router = APIRouter()

# Configuración de la base de datos
host = settings.HOST
user = settings.USERDB
password = settings.PASSWORD
database = settings.DATABASE

@router.post("/filter-by-genres", response_model=BooksOut)
def filter_books_by_genres(genres: list[str]) -> Any:
    """
    Retrieve books that match any of the genres provided in the list.
    """
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = conexion.cursor()

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

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")


@router.get("/{keyword}", response_model=BooksOut)
def read_top5_matched_books(keyword: str) -> Any:
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = conexion.cursor()

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



    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")


@router.get("/", response_model=BooksOut)
def read_books(skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve books with pagination.
    """
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = conexion.cursor()

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

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")


@router.get("/book/{book_id}", response_model=BookOut)
def read_book(book_id: int) -> Any:
    """
    Retrieve a specific book by its ID.
    """
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = conexion.cursor()

            # Consulta para obtener un libro por su ID
            query_book = """
                SELECT IdBook as id_book, Title as title, Authors as authors, Synopsis as synopsis, BuyLink as buy_link, 
                Genres as genres, Rating as rating, Editorial as editorial, Comments as comments, PublicationDate as publication_date, Image as image from Books
                WHERE IdBook = %s
            """
            cursor.execute(query_book, (book_id,))
            row = cursor.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Book not found with the provided id")

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

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")

@router.post("/books/{id}/comments")
def create_comment_rating(
    id: int,  # idBook
    user_id: int, 
    comment: str, 
    rating: int,
):
    try:
        # Validación de la calificación
        if not (1 <= rating <= 5):
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Verificar que el libro existe
            query_check_book = "SELECT IdBook FROM Books WHERE IdBook = %s"
            cursor.execute(query_check_book, (id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Book not found.")

            # Verificar que el usuario existe
            query_check_user = "SELECT id_user FROM users WHERE id_user = %s"
            cursor.execute(query_check_user, (user_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="User not found.")

            # Insertar comentario y calificación
            query_insert = """
                INSERT INTO CommentRatingPerBook (IdUser, IdBook, Comment, Rating)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_insert, (user_id, id, comment, rating))

            query_avg_rating = "SELECT AVG(Rating) FROM CommentRatingPerBook WHERE IdBook = %s"
            cursor.execute(query_avg_rating, (id,))
            avg_rating = cursor.fetchone()[0]

            query_update_book = "UPDATE Books SET Rating = %s WHERE IdBook = %s"
            cursor.execute(query_update_book, (avg_rating, id))
            conexion.commit()
            return {"message": "Comment and rating successfully added."}

    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error.")
    
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

@router.get("/CommentRatingPerBook/{idBook}")
def get_comments_ratings(idBook: int):
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Verificar que el libro existe
            query_check_book = "SELECT IdBook FROM Books WHERE IdBook = %s"
            cursor.execute(query_check_book, (idBook,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Book not found.")

            # Obtener los comentarios y calificaciones del libro
            query_get_comments = """
                SELECT crp.IdCommentRating, crp.IdUser, crp.Comment, crp.Rating, u.username
                FROM CommentRatingPerBook crp
                JOIN users u ON crp.IdUser = u.id_user
                WHERE crp.IdBook = %s
            """
            cursor.execute(query_get_comments, (idBook,))
            rows = cursor.fetchall()

            if not rows:
                return {"message": "No comments or ratings found for this book."}

            # Crear lista de respuestas
            comments_data = [
                {
                    "id_comment_rating": row[0],
                    "user_id": row[1],
                    "username": row[4],  # Incluyendo el nombre de usuario
                    "comment": row[2],
                    "rating": row[3]
                }
                for row in rows
            ]

            return {"comments": comments_data}

    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error.")
    
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


@router.post("/", response_model=BookOut)
def create_book(book_in: BookCreate) -> Any:
    """
    Create a new book.
    """
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = conexion.cursor()

            # Verificar si el libro ya existe por título
            query_check_book = "SELECT id_book FROM books WHERE title = %s"
            cursor.execute(query_check_book, (book_in.title,))
            existing_book = cursor.fetchone()

            if existing_book:
                raise HTTPException(
                    status_code=400,
                    detail="The book with this title already exists in the system."
                )
            # Insertar el nuevo libro en la base de datos
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

            # Confirmar la transacción
            conexion.commit()

            # Obtener el ID del libro recién creado
            new_book_id = cursor.lastrowid

            # Crear el objeto de salida BookOut
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
                publication_date=book_in.publication_date.isoformat() if book_in.publication_date else None,
                image=book_in.image
            )

            return book_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")


@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, book_in: BookUpdate) -> Any:
    """
    Update an existing book by its ID.
    """
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = conexion.cursor()

            # Verificar si el libro existe por su ID
            query_check_book = "SELECT IdBook as id_book FROM books WHERE IdBook = %s"
            cursor.execute(query_check_book, (book_id,))
            existing_book = cursor.fetchone()

            if not existing_book:
                raise HTTPException(
                    status_code=404,
                    detail="Book not found with the provided id"
                )

            # Actualizar el libro
            query_update_book = """
                UPDATE books SET Title = %s, Authors = %s, Synopsis = %s, BuyLink = %s, Genres = %s, Rating = %s,
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

            # Confirmar la transacción
            conexion.commit()

            # Obtener los datos actualizados
            '''
            
                WHERE IdBook = %s
            '''
            query_updated_book = """SELECT IdBook as id_book, Title as title, Authors as authors, Synopsis as synopsis, BuyLink as buy_link, 
                Genres as genres, Rating as rating, Editorial as editorial, Comments as comments, PublicationDate as publication_date, Image as image from Books WHERE IdBook = %s"""
            cursor.execute(query_updated_book, (book_id,))
            row = cursor.fetchone()

            # Crear el objeto de salida BookOut con los datos actualizados
            updated_book_out = BookOut(
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

            return updated_book_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")


@router.delete("/{book_id}", response_model=BookOut)
def delete_book(book_id: int) -> Any:
    """
    Delete a book by its ID.
    """
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = conexion.cursor()

            # Verificar si el libro existe
            query_check_book = "SELECT IdBooks FROM Books WHERE IdBook = %s"
            cursor.execute(query_check_book, (book_id,))
            existing_book = cursor.fetchone()

            if not existing_book:
                raise HTTPException(
                    status_code=404,
                    detail="Book not found with the provided id"
                )

            # Eliminar el libro
            query_delete_book = "DELETE FROM Books WHERE IdBook = %s"
            cursor.execute(query_delete_book, (book_id,))

            # Confirmar la transacción
            conexion.commit()

            # Devolver el libro eliminado
            deleted_book = BookOut(
                id_book=book_id,
                title="Deleted",
                authors="Deleted",
                synopsis="Deleted",
                buy_link="Deleted",
                genres="Deleted",
                rating=0,
                editorial="Deleted",
                comments="Deleted",
                publication_date="Deleted",
                image="Deleted"
            )

            return deleted_book

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")