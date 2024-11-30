""" Authenticated related dependencies """
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from mysql.connector import MySQLConnection

from app.core import security
from app.core.config import settings
from app.core.db import get_db_connection
from app.models import User, TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    """ Get a db connection to the db and yield the session """
    db_connection = get_db_connection()
    print('DB connection established')

    if db_connection.is_connected():
        print('Successfully connected to db')
        try:
            yield db_connection
        finally:
            db_connection.close()
            print('DB connection closed')


SessionDep = Annotated[MySQLConnection, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    cursor = session.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id_user = %s", (token_data.sub,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
