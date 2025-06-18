from pydantic import BaseModel, HttpUrl
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class DocumentBase(BaseModel):
    summary_title: str  # title from the beginning of the summary [:]
    summary: str  # generated summary of the document
    document_url: HttpUrl  # downloadable url of the document stored in S3
    document_name: str  # name of the uploaded document
    document_size: int  # size of the document in KB
    summary_length: str  # short, medium, or long
    date: datetime  # timestamp of when the document was uploaded


class DocumentCreate(DocumentBase):
    user_uuid: UUID


class Document(DocumentBase):
    id: UUID
    user_uuid: UUID

    class Config:
        orm_mode = True
