""" SignUp related routes """
from fastapi import APIRouter, HTTPException
import mysql.connector
import bcrypt
from app.api.deps import SessionDep
from app.models import UserCreate, UserOut
from typing import Any

router = APIRouter()

@router.post("/signup", response_model=UserOut)
def signup_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Sign up a new user with email and password.
    """
    try:
        cursor = session.cursor()

        # Check if the email or username already exists
        query_existing_user = "SELECT id_user FROM users WHERE email = %s OR username = %s"
        cursor.execute(query_existing_user, (user_in.email, user_in.username))
        existing_user_row = cursor.fetchone()

        if existing_user_row:
            raise HTTPException(
                status_code=400,
                detail="Email or username already exists.",
            )

        # Hash the password
        hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), bcrypt.gensalt())
        # Insert the new user into the database
        insert_user_query = """
        INSERT INTO users (name, surname, username, email, password) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_user_query, (
            user_in.name,
            user_in.surname,
            user_in.username,
            user_in.email,
            hashed_password,
        ))
        session.commit()  # Commit the transaction

        # Get the id of the new user
        new_user_id = cursor.lastrowid

        # Return the created user object
        user_out = UserOut(
            id_user=new_user_id,
            name=user_in.name,
            surname=user_in.surname,
            username=user_in.username,
            email=user_in.email
        )

        print("User signed up successfully")
        return user_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")
    except Exception as ex:
        print(f"Error al crear el usuario: {ex}")
        raise HTTPException(status_code=400, detail=str(ex))

    finally:
        if session.is_connected():
            cursor.close()
