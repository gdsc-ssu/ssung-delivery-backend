from typing import Callable

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import create_session
from domain.crew.crew_crud import get_crew
from domain.sender.sender_crud import get_sender
from models import Sender, Crew
from utils import get_token_subject

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

sender_scheme = OAuth2PasswordBearer(tokenUrl="/api/sender/login")
crew_scheme = OAuth2PasswordBearer(tokenUrl="/api/crew/login")


def get_auth_entity(
        get_entity: Callable[[Session, str], Sender | Crew | None],
        token: str,
        session: Session,
) -> Sender | Crew:
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
    return get_auth_entity(get_sender, token, session)


def get_auth_crew(
        token: str = Depends(crew_scheme),
        session: Session = Depends(create_session),
) -> Crew:
    return get_auth_entity(get_crew, token, session)