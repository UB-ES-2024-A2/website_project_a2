from typing import Any
from fastapi import APIRouter, HTTPException
import mysql.connector

from app.models import BookCreate, BookOut, BooksOut, BookUpdate

from app.api.deps import SessionDep
from app import crud

router = APIRouter()

@router.post("/filter-by-genres", response_model=BooksOut)
def filter_books_by_genres(session: SessionDep, genres: list[str]) -> Any:
    """
    Retrieve books that match any of the genres provided in the list.
    """
    try:
        cursor = session.cursor()
        return crud.book.get_books_by_genres(cursor=cursor, genres=genres)

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()


@router.get("/{keyword}", response_model=BooksOut)
def read_top5_matched_books(session: SessionDep, keyword: str) -> Any:
    try:
        cursor = session.cursor()

        return crud.book.get_books_by_key(cursor=cursor, keyword=keyword)

    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {err}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()


@router.get("/", response_model=BooksOut)
def read_books(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve books with pagination.
    """
    try:
        cursor = session.cursor()

        return crud.book.get_all_books(cursor=cursor, skip=skip, limit=limit)

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()


@router.get("/book/{book_id}", response_model=BookOut)
def read_book(session: SessionDep, book_id: int) -> Any:
    """
    Retrieve a specific book by its ID.
    """
    try:
        cursor = session.cursor()

        row = crud.book.get_book_by_id(cursor=cursor, book_id=book_id)

        if not row:
            raise HTTPException(status_code=404, detail="Book not found with the provided id")

        return row

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()

@router.post("/books/{id}/comments")
def create_comment_rating(
    session: SessionDep,
    id: int,  # idBook
    user_id: int,
    comment: str,
    rating: int,
):
    try:
        cursor = session.cursor()

        # Validación de la calificación
        if not (1 <= rating <= 5):
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

        # Verificar que el libro existe
        if not crud.book.get_book_by_id(cursor=cursor, book_id=id):
            raise HTTPException(status_code=404, detail="Book not found.")

        # Verificar que el usuario existe
        if not crud.user.get_user_by_id(cursor=cursor, user_id=user_id):
            raise HTTPException(status_code=404, detail="User not found.")

        # Insertar comentario y calificación
        crud.rating.create_rating(cursor=cursor, id=id, user_id=user_id, comment=comment, rating=rating)
        session.commit()

        return {"message": "Comment and rating successfully added."}

    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error.")

    finally:
        if session.is_connected():
            cursor.close()

@router.get("/CommentRatingPerBook/{idBook}")
def get_comments_ratings(
        session: SessionDep,
        idBook: int):
    try:
        cursor = session.cursor()

        # Verificar que el libro existe
        if not crud.book.get_book_by_id(cursor=cursor, book_id=idBook):
            raise HTTPException(status_code=404, detail="Book not found.")

        # Obtener los comentarios y calificaciones del libro
        rows = crud.rating.get_ratings(cursor=cursor, book_id=idBook)

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
        if session.is_connected():
            cursor.close()

@router.post("/", response_model=BookOut)
def create_book(session: SessionDep, book_in: BookCreate) -> Any:
    """
    Create a new book.
    """
    try:
        cursor = session.cursor()

        # Verificar si el libro ya existe por título
        existing_book = crud.book.get_book_by_title(cursor=cursor, book_title=book_in.title)

        if existing_book:
            raise HTTPException(
                status_code=400,
                detail="The book with this title already exists in the system."
            )

        book_out = crud.book.create_book(cursor=cursor, book_in=book_in)

        # Confirmar la transacción
        session.commit()


        return book_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()


@router.put("/{book_id}", response_model=BookOut)
def update_book(session: SessionDep, book_id: int, book_in: BookUpdate) -> Any:
    """
    Update an existing book by its ID.
    """
    try:
        cursor = session.cursor()

        # Verificar si el libro existe por su ID
        existing_book = crud.book.get_book_by_id(cursor=cursor, book_id=book_id)

        if not existing_book:
            raise HTTPException(
                status_code=404,
                detail="Book not found with the provided id"
            )

        # Actualizar el libro
        updated_book_out = crud.book.update_book(cursor=cursor, book_id=book_id, book_in=book_in)

        # Confirmar la transacción
        session.commit()

        return updated_book_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()


@router.delete("/{book_id}")
def delete_book(session: SessionDep, book_id: int) -> Any:
    """
    Delete a book by its ID.
    """
    try:
        cursor = session.cursor()

        # Verificar si el libro existe
        existing_book = crud.book.get_book_by_id(cursor=cursor, book_id=book_id)

        if not existing_book:
            raise HTTPException(
                status_code=404,
                detail="Book not found with the provided id"
            )

        # Eliminar el libro
        crud.book.delete_book(cursor=cursor, book_id=book_id)

        # Confirmar la transacción
        session.commit()

        return {"message": "Book successfully deleted."}

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()

@router.delete("/CommentRatingPerBook/{comment_id}")
def delete_comment(session: SessionDep, comment_id: int):
    """
    Delete a rating book by its ID.
    """
    try:
        cursor = session.cursor()

        # Verificar que el comentario existe
        result = crud.rating.get_rating_by_id(cursor=cursor, comment_id=comment_id)
        if not result:
            raise HTTPException(status_code=404, detail="Comment not found.")

        # Obtener el IdBook del comentario
        id_book = result[0]

        # Eliminar el comentario
        crud.rating.delete_rating(cursor=cursor, comment_id=comment_id)

        # Recalcular el promedio de calificación
        crud.rating.calculate_rating(cursor=cursor, book_id=id_book)

        # Actualizar el promedio en la tabla de libros
        avg_rating = cursor.fetchone()[0] or 0
        crud.book.update_avg(cursor=cursor, id_book=id_book, avg_rating=avg_rating)

        session.commit()
        return {"message": "Comment successfully deleted."}

    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error.")

    finally:
        if session.is_connected():
            cursor.close()

@router.get("/books/ratings/{idUser}")
def get_books_ratings_by_user(
        session: SessionDep,
        idUser: int,
        skip: int = 0,
        limit: int = 100):
    try:
        cursor = session.cursor()

        # Verificar que el usuario existe
        if not crud.user.get_user_by_id(cursor=cursor, user_id=idUser):
            raise HTTPException(status_code=404, detail="User not found.")

        # Obtener los libros y calificaciones del usuario
        rows = crud.rating.get_books_with_ratings_by_user(cursor=cursor, user_id=idUser, skip=skip, limit=limit)

        if not rows:
            return {"message": "No ratings found for this user."}

        # Crear lista de respuestas
        books_data = [
            {
                "book": {
                    "id_book": row["book"]["id_book"],
                    "title": row["book"]["title"],
                    "authors": row["book"]["authors"],
                    "synopsis": row["book"]["synopsis"],
                    "buy_link": row["book"]["buy_link"],
                    "genres": row["book"]["genres"],
                    "rating": float(row["book"]["rating"]) if row["book"]["rating"] else None,
                    "editorial": row["book"]["editorial"],
                    "comments": row["book"]["comments"],
                    "publication_date": row["book"]["publication_date"],
                    "image": row["book"]["image"]
                },
                "user_rating": row["user_rating"] if row["user_rating"] else None
            }
            for row in rows['data']
        ]

        return {"data": books_data, "count": len(books_data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))