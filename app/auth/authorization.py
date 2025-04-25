from app.auth.fake_users import fake_users
from app.auth.auth_utils import verify_password
from app.auth.jwt import (
    create_access_token,
    create_jwt,
    create_refresh_token,
    decode_jwt,
)
from fastapi import HTTPException, status, Depends
from app.core.settings import settings
from fastapi import APIRouter
from app.schemas.user import UserSchemaLogin, UserSchemaResponse
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.token import TokenResponse
from datetime import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def check_user(username: str):
    current_user = fake_users.get(username)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return current_user


def authenticate_user(username: str, password: str):
    user = check_user(username)
    check_password = verify_password(password, user["password"])
    if not check_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован, доступ запрещен",
        )
    return user


# проверка времени жизни токена
def is_token_expired(expire_timestamp: int) -> bool:
    expire_time = datetime.fromtimestamp(expire_timestamp)
    return datetime.utcnow() > expire_time


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    decode_token: dict = decode_jwt(
        token=token,
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
    )
    username = decode_token["sub"]
    user = check_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован",
            headers={"WWW-Authenticate": "Bearer"},
        )
    current_user = UserSchemaResponse(
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
    )
    return current_user


@router.post("/login", response_model=TokenResponse)
def login(data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(data.username, data.password)
    user_data = UserSchemaLogin(
        username=data.username,
        password=data.password,
    )
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/users/me")
def read_user(
    current_user: Annotated[UserSchemaResponse, Depends(get_current_user)],
):
    return current_user
