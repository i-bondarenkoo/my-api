import jwt
from app.core.settings import settings
from datetime import datetime, timedelta
from app.schemas.user import UserSchemaLogin

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


# функция создания токена
def create_jwt(
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
        key=secret_key,
    )
    return token


# функция декодирования токена
def decode_jwt(
    token: str | bytes,
    secret_key: str = settings.secret_key,
    algorithm: str = settings.algorithm,
):
    decode_token = jwt.decode(
        jwt=token,
        key=secret_key,
        algorithms=[algorithm],
    )
    return decode_token


def create_access_token(token_data: UserSchemaLogin) -> str:
    jwt_payload = {
        "sub": token_data.username,
        "type": ACCESS_TOKEN_TYPE,
    }
    access_token = create_jwt(
        payload=jwt_payload,
        algorithm=settings.algorithm,
        secret_key=settings.secret_key,
        expire_minutes=settings.access_token_expire_minutes,
    )
    return access_token


def create_refresh_token(token_data: UserSchemaLogin) -> str:
    jwt_payload = {
        "sub": token_data.username,
        "type": REFRESH_TOKEN_TYPE,
    }
    refresh_token = create_jwt(
        payload=jwt_payload,
        algorithm=settings.algorithm,
        secret_key=settings.secret_key,
        expire_timedelta=timedelta(days=settings.refresh_token_expire_days),
    )
    return refresh_token
