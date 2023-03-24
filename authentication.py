from typing import Callable, Optional, TypeVar, ParamSpec

from fastapi import HTTPException, Depends
from jose import JWTError
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordBearer

from database import create_session
from domain.crew.crew_query import select_crew
from domain.sender.sender_query import select_sender
from models import Sender, Crew
from utils import get_token_subject

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

sender_scheme = OAuth2PasswordBearer(tokenUrl="/sender/login")
crew_scheme = OAuth2PasswordBearer(tokenUrl="/crew/login")

T = TypeVar("T", Sender, Crew)
P = ParamSpec("P")


def get_auth_entity(
    get_entity: Callable[P, Optional[T]],
    token: str,
    session: Session,
) -> T:
    try:
        username = get_token_subject(token)
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    entity = get_entity(session, username)
    if entity is None:
        raise credentials_exception

    return entity


def get_auth_sender(
    token: str = Depends(sender_scheme),
    session: Session = Depends(create_session),
) -> Sender:
    return get_auth_entity(select_sender, token, session)


def get_auth_crew(
    token: str = Depends(crew_scheme),
    session: Session = Depends(create_session),
) -> Crew:
    return get_auth_entity(select_crew, token, session)
