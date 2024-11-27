""" User management routes """
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.models import (
    UserCreate,
    UserOut,
    UsersOut,
    UserUpdate
)

import mysql.connector
import bcrypt

router = APIRouter()

@router.get("/{keyword}", response_model=UsersOut)
def read_top5_matched_users(session: SessionDep, keyword: str) -> Any:
    try:
        # Conexión a la base de datos
        cursor = session.cursor()

        # Crear la consulta de búsqueda
        query = """
            SELECT id_user, name, surname, username, email
               FROM users
               WHERE name LIKE %s OR surname LIKE %s or username LIKE %s
               LIMIT 5;
        """

        # Preparar el parámetro de búsqueda con el carácter comodín
        search_param = f"%{keyword}%"

        # Ejecutar la consulta
        cursor.execute(query, (search_param, search_param, search_param))

        # Obtener los resultados
        resultados = cursor.fetchall()

        # Contar el total de libros
        query_count = "SELECT COUNT(1) FROM Books"
        cursor.execute(query_count)
        count = cursor.fetchone()[0]

        users_data = [
            UserOut(
                id_user=row[0],
                name=row[1],
                surname=row[2],
                username=row[3],
                email=row[4]
            ) for row in resultados
        ]

        return UsersOut(data=users_data, count=count)
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

        query_user = """
            SELECT id_user, name, surname, username, email 
            FROM users 
            WHERE id_user = %s
        """
        cursor.execute(query_user, (user_id,))
        row = cursor.fetchone()

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

@router.get("/")
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    try:
        cursor = session.cursor()

        # Update query to fetch users
        query_users = "SELECT id_user, name, surname, username, email FROM users LIMIT %s OFFSET %s"
        cursor.execute(query_users, (limit, skip))
        filas = cursor.fetchall()

        # Count the total number of users
        query_count = "SELECT COUNT(1) FROM users"
        cursor.execute(query_count)
        count = cursor.fetchone()[0]

        # Transform tuples to a list of UserOut
        users_data = [
            UserOut(
                id_user=row[0],
                name=row[1],
                surname=row[2],
                username=row[3],
                email=row[4]
            ) for row in filas
        ]

        return UsersOut(data=users_data, count=count)

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
    try:
            cursor = session.cursor()

            # Verificar si el usuario existe
            query_check_user = "SELECT id_user FROM users WHERE id_user = %s"
            cursor.execute(query_check_user, (user_id,))
            existing_user = cursor.fetchone()

            if not existing_user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found with the provided ID",
                )

            update_fields = []
            update_values = []

            if user_in.name is not None:
                update_fields.append("name = %s")
                update_values.append(user_in.name)
            if user_in.surname is not None:
                update_fields.append("surname = %s")
                update_values.append(user_in.surname)
            if user_in.username is not None:
                update_fields.append("username = %s")
                update_values.append(user_in.username)
            if user_in.email is not None:
                update_fields.append("email = %s")
                update_values.append(user_in.email)
            if user_in.password is not None:
                hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), bcrypt.gensalt())
                update_fields.append("password = %s")
                update_values.append(hashed_password)

            if not update_fields:
                raise HTTPException(
                    status_code=400,
                    detail="No fields provided for update",
                )

            # Crear la consulta dinámica
            query_update_user = f"""
                UPDATE users
                SET {', '.join(update_fields)}
                WHERE id_user = %s
            """
            update_values.append(user_id)
            cursor.execute(query_update_user, tuple(update_values))
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
        query_check_user = "SELECT id_user FROM users WHERE email = %s"
        cursor.execute(query_check_user, (user_in.email,))
        existing_user = cursor.fetchone()

        if existing_user:
            print("El usuario ya existe")
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

        # Insertar el nuevo usuario en la base de datos
        query_create_user = """
            INSERT INTO users (name, surname, username, email, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(query_create_user, (
            user_in.name,
            user_in.surname,
            user_in.username,
            user_in.email,
            hashed_password
        ))

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

@router.get("/by-email", response_model=UserOut)
def read_user_by_email(*, session: SessionDep, email: str) -> Any:
    """
    Get a user by email.
    """
    try:
        cursor = session.cursor()

        # Consulta para obtener el usuario por email
        query_user = "SELECT id_user, name, surname, username, email, password FROM users WHERE email = %s"
        cursor.execute(query_user, (email,))
        user_row = cursor.fetchone()

        if not user_row:
            raise HTTPException(
                status_code=404,
                detail="User not found with the provided email",
            )

        # Crear el objeto UserOut basado en los datos obtenidos
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
        raise HTTPException(status_code=400, detail=str(ex))

    finally:
        if session.is_connected():
            cursor.close()