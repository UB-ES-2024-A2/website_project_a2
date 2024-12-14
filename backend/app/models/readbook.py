from sqlmodel import Field, SQLModel
from typing import Optional

# Shared properties for ReadBooks
class ReadBookBase(SQLModel):
    id_user: int
    id_book: int

# Database model, table inferred from class name
class ReadBook(ReadBookBase, table=True):
    id_entry: int | None = Field(default=None, primary_key=True)

# Properties to receive via API on creation
class ReadBookCreate(ReadBookBase):
    pass

# Properties to receive via API on update, all are optional (you may extend this for future use)
class ReadBookUpdate(SQLModel):
    id_user: Optional[int] = None
    id_book: Optional[int] = None

# Properties to return via API
class ReadBookOut(ReadBookBase):
    id_entry: int
