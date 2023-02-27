from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import create_session
from domain.crew.crew_crud import get_crew
from domain.sender.sender_crud import get_sender
from models import Sender
from utils import get_token_subject

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

sender_scheme = OAuth2PasswordBearer(tokenUrl="/api/sender/login")
crew_scheme = OAuth2PasswordBearer(tokenUrl="/api/crew/login")


def get_current_sender(
        token: str = Depends(sender_scheme),
        session: Session = Depends(create_session),
) -> Sender:
    try:
        username = get_token_subject(token)
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    sender = get_sender(session, username)
    if sender is None:
        raise credentials_exception

    return sender


def get_current_crew(
        token: str = Depends(crew_scheme),
        session: Session = Depends(create_session),
) -> Sender:
    try:
        username = get_token_subject(token)
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    crew = get_crew(session, username)
    if crew is None:
        raise credentials_exception

    return crew
