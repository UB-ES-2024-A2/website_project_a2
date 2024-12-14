from typing import Any
from fastapi import APIRouter, HTTPException
import mysql.connector

from app.models import ReadBookCreate, ReadBookOut
from app.api.deps import SessionDep
from app import crud

router = APIRouter()

@router.post("/readbooks", response_model=ReadBookOut)
def create_readbook(session: SessionDep, readbook_in: ReadBookCreate) -> Any:
    """
    Create a new book entry for a user in the 'readbooks' table.
    """
    try:
        cursor = session.cursor()
        readbook_out = crud.readbooks.create_readbook(cursor=cursor, readbook_in=readbook_in)
        session.commit()

        return readbook_out

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()

@router.delete("/readbooks/{id_user}/{id_book}", response_model=bool)
def delete_user_readbook(session: SessionDep, id_user: int, id_book: int) -> Any:
    """
    Delete a book entry for a user based on user_id and book_id from the 'readbooks' table.
    """
    try:
        cursor = session.cursor()
        success = crud.readbooks.delete_user_readbook(cursor=cursor, id_user=id_user, id_book=id_book)
        
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

@router.get("/readbooks/{id_user}/{id_book}", response_model=ReadBookOut)
def get_readbook(session: SessionDep, id_user: int, id_book: int) -> Any:
    """
    Get a book entry for a user based on user_id and book_id from the 'readbooks' table.
    """
    try:
        cursor = session.cursor()
        readbook_out = crud.readbooks.get_readbook(cursor=cursor, id_user=id_user, id_book=id_book)
        
        if not readbook_out:
            raise HTTPException(status_code=404, detail="Entry not found")

        return readbook_out

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()
