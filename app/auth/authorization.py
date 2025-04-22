#  Создай функцию логина
# Эта функция будет:

# Принимать username и password (например, из Pydantic схемы)

# Искать пользователя в твоём fake_users_db

# Проверять, что пользователь существует

# Проверять пароль через verify_password(...)

# Если всё ок — звать create_access_token(...)

# Возвращать токен (обычно access_token и token_type)

# 📌 Это будет использоваться в POST /login.
from app.auth.fake_users import fake_users
from app.auth.auth_utils import verify_password
from app.auth.jwt import create_access_token
from fastapi import HTTPException, status, Depends
from app.core.settings import settings


def check_user(username: str, password: str, fake_users: dict):
    current_user = fake_users.get(username)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return current_user


def authenticate_user(fake_users, username: str, password: str):
    user = check_user(username, password, fake_users)
    check_password = verify_password(password, user["password"])
    if not check_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не авторизован, доступ запрещен",
        )
    return user


def login(username: str, password: str):
    user = authenticate_user(fake_users, username, password)
    new_token = create_access_token(
        payload={"sub": username},
        algorithm=settings.algorithm,
        secret_key=settings.secret_key,
    )
    return {"access_token": new_token, "token_type": "bearer"}
