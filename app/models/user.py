from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID, uuid4

from app.models.documents import Document

class User(BaseModel):
    uuid: UUID
    username: str
    disabled: Optional[bool] = False
    documents: Optional[List[Document]] = []

class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
