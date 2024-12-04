""" User management routes """
from typing import Any

from fastapi import APIRouter, HTTPException

import mysql.connector
import bcrypt

from app.api.deps import SessionDep
from app.models import (
    UserCreate,
    UserOut,
    UsersOut,
    UserUpdate
)
from app import crud

router = APIRouter()

@router.get("/{keyword}", response_model=UsersOut)
def read_top5_matched_users(session: SessionDep, keyword: str) -> Any:
    """
    Retrieve matched users by the keyword.
    """
    try:
        # Conexión a la base de datos
        cursor = session.cursor()

        return crud.user.read_top5_matched_users(cursor=cursor, keyword=keyword)

    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {err}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()

@router.get("/by-id/{user_id}", response_model=UserOut)
def read_user(session: SessionDep, user_id: int) -> Any:
    """
    Retrieve a specific user by its ID.
    """
    try:
        cursor = session.cursor()

        row = crud.user.get_user_by_id(cursor=cursor, user_id=user_id)

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="User not found with the provided id"
            )

        user_out = UserOut(
            id_user=row[0],
            name=row[1],
            surname=row[2],
            username=row[3],
            email=row[4],
        )
        return user_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")
    finally:
        if session.is_connected():
            cursor.close()

@router.get("/by-email/{user_mail}", response_model=UserOut)
def read_user_by_email(session: SessionDep, user_mail: str) -> Any:
    """
    Get a user by its email.
    """
    try:
        cursor = session.cursor()

        user_row = crud.user.get_user_by_email(cursor=cursor, email=user_mail)

        if not user_row:
            raise HTTPException(
                status_code=404,
                detail="User not found with the provided email"
            )

        # Create the UserOut object for the user read
        user_out = UserOut(
            id_user=user_row[0],
            name=user_row[1],
            surname=user_row[2],
            username=user_row[3],
            email=user_row[4],
        )

        return user_out
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")
    except Exception as ex:
        print(f"Error al obtener el usuario: {ex}")
        raise HTTPException(status_code=500, detail=str(ex))

    finally:
        if session.is_connected():
            cursor.close()

@router.get("/")
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    try:
        cursor = session.cursor()

        return crud.user.read_users(cursor=cursor, skip=skip, limit=limit)

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")

    finally:
        if session.is_connected():
            cursor.close()

@router.put("/{user_id}")
def update_user_fields(
    session: SessionDep,
    user_id: int,
    user_in: UserUpdate,
) -> Any:
    """
    Update user fields.
    """
    try:
        cursor = session.cursor()

        # Verificar si el usuario existe
        existing_user = crud.user.get_user_by_id(cursor=cursor, user_id=user_id)

        if not existing_user:
            raise HTTPException(
                status_code=404,
                detail="User not found with the provided ID",
            )

        update_fields = crud.user.update_user(cursor=cursor, user_id=user_id, user_in=user_in)

        if not update_fields:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update",
            )

        session.commit()

        return {"message": "User updated successfully"}

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")
    except Exception as ex:
        print(f"Error inesperado: {ex}")
        raise HTTPException(status_code=400, detail=str(ex))
    finally:
        if session.is_connected():
            cursor.close()


@router.post(
    "/",
    response_model=UserOut
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    try:
        cursor = session.cursor()

        # Verificar si el usuario ya existe por email
        existing_user = crud.user.get_user_by_email(cursor=cursor, email=user_in.email)

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

        crud.user.create_user(cursor=cursor, user_in=user_in)

        # Confirmar la transacción
        session.commit()

        # Obtener el ID del usuario recién creado
        new_user_id = cursor.lastrowid

        # Crear el objeto de salida
        user_out = UserOut(
            id_user=new_user_id,
            name=user_in.name,
            surname=user_in.surname,
            username=user_in.username,
            email=user_in.email
        )
        '''
        # Enviar correo si está habilitado
        if settings.emails_enabled and user_in.email:
            email_data = generate_new_account_email(
                email_to=user_in.email, username=user_in.email, password=user_in.password
            )
            send_email(
                email_to=user_in.email,
                subject=email_data.subject,
                html_content=email_data.html_content,
            )
        '''
        return user_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if session.is_connected():
            cursor.close()
