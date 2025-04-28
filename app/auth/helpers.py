from fastapi import HTTPException, status
from functools import wraps
from jwt.exceptions import ExpiredSignatureError


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Время действия access токена истекло",
            )

    return wrapper
