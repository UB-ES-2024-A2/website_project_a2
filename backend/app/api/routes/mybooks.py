from typing import Any
from fastapi import APIRouter, HTTPException
import mysql.connector

from app.models import MyBookCreate, MyBookOut, MyBooksOut, BooksOut
from app.api.deps import SessionDep
from app import crud

router = APIRouter()

@router.post("/mybooks", response_model=MyBookOut)
def create_mybook(session: SessionDep, mybook_in: MyBookCreate) -> Any:
    """
    Create a new book entry for a user in the 'mybooks' table.
    """
    try:
        cursor = session.cursor()
        mybook_out = crud.mybooks.create_mybook(cursor=cursor, mybook_in=mybook_in)
        session.commit()

        return mybook_out

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()

@router.delete("/mybooks/{id_user}/{id_book}", response_model=bool)
def delete_user_book(session: SessionDep, id_user: int, id_book: int) -> Any:
    """
    Delete a book entry for a user based on user_id and book_id from the 'mybooks' table.
    """
    try:
        cursor = session.cursor()
        success = crud.mybooks.delete_user_book(cursor=cursor, id_user=id_user, id_book=id_book)
        
        if not success:
            raise HTTPException(status_code=404, detail="Entry not found")

        session.commit()
        return success

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()

@router.get("/{id_user}", response_model=BooksOut)
def get_mybooks(session: SessionDep, id_user: int) -> Any:
    """
    Get all books entry for a user based on user_id from the 'mybooks' table.
    """
    try:
        cursor = session.cursor()
        mybook_out = crud.mybooks.get_mybooks(cursor=cursor, id_user=id_user)
        
        if not mybook_out:
            raise HTTPException(status_code=404, detail="Entry not found")

        # Inicializar una lista para los libros
        books_data = []

        # Obtener información de cada libro utilizando id_book de mybook_out
        for mybook in mybook_out.data:
            book_details = crud.book.get_book_by_id(cursor=cursor, book_id=mybook.id_book)
            if book_details:
                books_data.append(book_details)
            else:
                print(f"Book with id {mybook.id_book} not found.")

        # Crear y devolver la respuesta BooksOut con los libros obtenidos
        return BooksOut(data=books_data, count=len(books_data))

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()
