""" Main API routes definition """
from fastapi import APIRouter

from app.api.routes import login, users, books, signup, mybooks, readbooks

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(signup.router, tags=["signup"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(mybooks.router, prefix="/mybooks", tags=["mybooks"])
api_router.include_router(readbooks.router, prefix="/readbooks", tags=["readbooks"]) 
