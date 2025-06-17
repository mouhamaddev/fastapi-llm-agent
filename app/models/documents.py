from pydantic import BaseModel, HttpUrl
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class DocumentBase(BaseModel):
    summary_title: str
    summary: str
    document_url: HttpUrl
    document_name: str
    document_size: int
    summary_length: int
    date: datetime


class DocumentCreate(DocumentBase):
    user_uuid: UUID


class Document(DocumentBase):
    id: UUID
    user_uuid: UUID

    class Config:
        orm_mode = True
