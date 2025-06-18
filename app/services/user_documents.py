import os
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID, uuid4

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.models.user import User, UserInDB, TokenData
from app.models.documents import Document, DocumentCreate

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
users_table = dynamodb.Table("users")
documents_table = dynamodb.Table("documents")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(username: str) -> Optional[UserInDB]:
    try:
        response = users_table.get_item(Key={"username": username})
        user_item = response.get("Item")
        if user_item:
            return UserInDB(
                uuid=user_item["uuid"],
                username=user_item["username"],
                disabled=user_item.get("disabled", False),
                documents=[],
                hashed_password=user_item["hashed_password"],
            )
        return None
    except ClientError as e:
        print(f"DynamoDB get_user error: {e.response['Error']['Message']}")
        return None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[UserInDB]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except JWTError:
        return None

    user = get_user(token_data.username)
    if user is None:
        return None

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_user(username: str, password: str) -> UserInDB:
    existing_user = get_user(username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(password)
    new_user_uuid = str(uuid4())

    user_item = {
        "uuid": new_user_uuid,
        "username": username,
        "hashed_password": hashed_password,
        "disabled": False,
    }

    try:
        users_table.put_item(Item=user_item)
    except ClientError as e:
        print(f"DynamoDB create_user error: {e.response['Error']['Message']}")
        raise HTTPException(status_code=500, detail="Failed to create user")

    return UserInDB(
        uuid=new_user_uuid,
        username=username,
        hashed_password=hashed_password,
        disabled=False,
        documents=[],
    )


def get_uuid_by_username(username: str) -> Optional[str]:
    user = get_user(username)
    if user:
        return user.uuid
    return None

# Document functions

def create_document(document_create: DocumentCreate) -> Document:
    new_document_id = str(uuid4())

    item = {
        "id": new_document_id,
        "user_uuid": str(document_create.user_uuid),
        "summary_title": document_create.summary_title,
        "summary": document_create.summary,
        "document_url": str(document_create.document_url),
        "document_name": document_create.document_name,
        "document_size": document_create.document_size,
        "summary_length": document_create.summary_length,
        "date": document_create.date.isoformat(),
    }

    try:
        documents_table.put_item(Item=item)
    except ClientError as e:
        print(f"DynamoDB create_document error: {e.response['Error']['Message']}")
        raise HTTPException(status_code=500, detail="Failed to create document")

    return Document(**item)


def get_documents_for_user(user_uuid: UUID) -> List[Document]:
    try:
        response = documents_table.query(
            IndexName="user_uuid-index",
            KeyConditionExpression=Key("user_uuid").eq(str(user_uuid)),
        )
        items = response.get("Items", [])
        documents = []
        for item in items:
            item["date"] = datetime.fromisoformat(item["date"])
            documents.append(Document(**item))
        return documents
    except ClientError as e:
        print(f"DynamoDB get_documents_for_user error: {e.response['Error']['Message']}")
        raise HTTPException(status_code=500, detail="Failed to get documents")


def attach_documents_to_user(user: UserInDB) -> User:
    documents = get_documents_for_user(UUID(user.uuid))
    return User(
        uuid=user.uuid,
        username=user.username,
        disabled=user.disabled,
        documents=documents,
    )
