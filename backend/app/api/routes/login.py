""" Login related routes """
from typing import Any

from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.models import UserOut
import mysql.connector
import bcrypt

router = APIRouter()

@router.post("/login", response_model=UserOut)
def login_user(*, session: SessionDep, email: str, pswd_input: str) -> Any:
    """
    Login a user by email and password.
    """
    try:
            cursor = session.cursor()

            # Consulta para obtener el hash de la contraseña del usuario por email
            query_user = "SELECT id_user, name, surname, username, email, password FROM users WHERE email = %s"
            cursor.execute(query_user, (email,))
            user_row = cursor.fetchone()

            if not user_row:
                raise HTTPException(
                    status_code=404,
                    detail="User not found with the provided email",
                )

            # Extraer el hash almacenado y verificar la contraseña ingresada
            stored_hashed_password = user_row[5].encode('utf-8')

            # Verificar la contraseña ingresada contra el hash almacenado
            if not bcrypt.checkpw(pswd_input.encode('utf-8'), stored_hashed_password):
                raise HTTPException(
                    status_code=400,
                    detail="Incorrect password.",
                )

            # Crear el objeto UserOut basado en los datos obtenidos si la contraseña es correcta
            user_out = UserOut(
                id_user=user_row[0],  # id_user
                name=user_row[1],  # name
                surname=user_row[2],  # surname
                username=user_row[3],  # username
                email=user_row[4]  # email
            )

            print("Inicio de sesión exitoso")
            return user_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")
    except Exception as ex:
        print(f"Error al verificar el usuario: {ex}")
        raise HTTPException(status_code=400, detail=str(ex))

    finally:
        if session.is_connected():
            cursor.close()