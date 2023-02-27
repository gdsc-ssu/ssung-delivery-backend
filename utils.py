from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(subject: str | Any, expires_delta: timedelta = None) -> str:
    now = datetime.utcnow()
    if expires_delta:
        expires_delta = now + expires_delta
    else:
        expires_delta = now + \
                        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def get_token_subject(token: str) -> str:
    return jwt.decode(
        token=token,
        algorithms=settings.ALGORITHM,
        key=settings.JWT_SECRET_KEY
    ).get("sub")
