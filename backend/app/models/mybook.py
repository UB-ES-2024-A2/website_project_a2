""" MyBooks models """
from sqlmodel import Field, SQLModel
from typing import Optional

# Shared properties for MyBooks
class MyBookBase(SQLModel):
    id_user: int
    id_book: int

# Database model, table inferred from class name
class MyBook(MyBookBase, table=True):
    id_entry: int | None = Field(default=None, primary_key=True)

# Properties to receive via API on creation
class MyBookCreate(MyBookBase):
    pass

# Properties to receive via API on update, all are optional (you may extend this for future use)
class MyBookUpdate(SQLModel):
    id_user: Optional[int] = None
    id_book: Optional[int] = None

# Properties to return via API
class MyBookOut(MyBookBase):
    id_entry: int

class MyBooksOut(SQLModel):
    data: list[MyBookOut]
    count: int
