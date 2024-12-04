""" User related CRUD methods """
from typing import Any
import bcrypt

from app.models import User, UserCreate, UserUpdate, UserOut, UsersOut


def create_user(*, cursor, user_in: UserCreate) -> None:
    """
    Creates a new user in the database using the provided user data.

    Args:
        cursor (cursor): The database cursor to execute the SQL query.
        user_in (UserCreate): An object containing the user's details to be created, such as name, surname, username, email, and password.

    Returns:
        None: This function does not return a value; it performs the database operation directly.
    """
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

def get_user_by_id(*, cursor, user_id: int) -> Any:
    """
    Retrieves a user from the database by their ID.

    Args:
        cursor (cursor): The database cursor to execute the SQL query.
        user_id (int): The ID of the user to be retrieved.

    Returns:
        Any: The user record if found, or None if the user does not exist.
    """
    query_check_user = "SELECT * FROM users WHERE id_user = %s"
    cursor.execute(query_check_user, (user_id,))
    existing_user = cursor.fetchone()

    return existing_user
def update_user(*, cursor, user_id: int, user_in: UserUpdate) -> Any:
    """
    Updates an existing user in the database with the provided details.

    Args:
        cursor (cursor): The database cursor to execute the SQL query.
        user_id (int): The ID of the user to be updated.
        user_in (UserUpdate): An object containing the updated user data.

    Returns:
        Any: A success message if the update is successful, or None if no fields were updated.
    """
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
        return None

    # Crear la consulta dinámica
    query_update_user = f"""
                UPDATE users
                SET {', '.join(update_fields)}
                WHERE id_user = %s
            """
    update_values.append(user_id)
    cursor.execute(query_update_user, tuple(update_values))

    return "User updated successfully"


def get_user_by_email(*, cursor, email: str) -> User | None:
    """
    Retrieves a user from the database by their email address.

    Args:
        cursor (cursor): The database cursor to execute the SQL query.
        email (str): The email address of the user to be retrieved.

    Returns:
        User | None: The user record if found, or None if the user does not exist.
    """
    query_check_user = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query_check_user, (email,))
    existing_user = cursor.fetchone()

    return existing_user

def read_users(*, cursor, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieves a list of users from the database with pagination.

    Args:
        cursor (cursor): The database cursor to execute the SQL queries.
        skip (int): The number of records to skip (default is 0).
        limit (int): The number of records to return (default is 100).

    Returns:
        Any: A UsersOut object containing a list of user data and the total count of users.
    """
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

def read_top5_matched_users(*, cursor,  keyword: str) -> Any:
    """
    Retrieves the top 5 users from the database whose name, surname, or username matches the provided keyword.

    Args:
        cursor (cursor): The database cursor to execute the SQL queries.
        keyword (str): The keyword to search for in the name, surname, or username fields.

    Returns:
        Any: A UsersOut object containing a list of matched users and the total count of books in the database.
    """
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
