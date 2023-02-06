from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from typing import Any, Union
from os import getenv

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    now = datetime.utcnow()
    if expires_delta:
        expires_delta = now + expires_delta
    else:
        expires_delta = now + \
            timedelta(minutes=getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, getenv(
        'JWT_SECRET_KEY'), getenv('ALGORITHM'))
    return encoded_jwt
