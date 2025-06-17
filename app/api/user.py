from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from app.services import user_documents
from app.models.user import User, UserCreate, UserInDB, Token

router = APIRouter()


@router.post("/register", response_model=User)
def register(user: UserCreate):
    """
    Register a new user with username and password.
    """
    try:
        user = user_documents.create_user(user.username, user.password)
    except HTTPException as e:
        raise e

    return User(
        uuid=user.uuid,
        username=user.username,
        disabled=user.disabled,
        documents=[],
    )


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login user and return JWT access token.
    OAuth2PasswordRequestForm expects form fields: username and password
    """
    user: UserInDB = user_documents.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=user_documents.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = user_documents.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")