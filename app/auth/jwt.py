import jwt
from app.core.settings import settings
from datetime import datetime, timedelta


# функция создания токена
def create_access_token(
    payload: dict,
    algorithm: str = settings.algorithm,
    secret_key: str = settings.secret_key,
    expire_minutes: int = settings.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    token = jwt.encode(
        payload=to_encode,
        algorithm=algorithm,
        secret_key=secret_key,
    )
    return token


# функция декодирования токена
def decode_access_token(
    token: str | bytes,
    secret_key: str = settings.secret_key,
    algorithm: str = settings.algorithm,
):
    decode_token = jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
    )
    return decode_token
