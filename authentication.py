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

#함수 이름 auth_sender로 변경해주세요. sender를 가져오니까 get_current도 괜찮지만, 함수의 주 목적이 가져오는 것 보다는 auth에 초점이 맞춰져 있기 때문에
#auth 키워드를 가져가는게 좋아 보입니다.

def get_auth_sender(
        token: str = Depends(sender_scheme),
        session: Session = Depends(create_session),
) -> Sender:
    try:
        sender_name = get_token_subject(token)
        if sender_name is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    sender = get_sender(session, sender_name)
    if sender is None:
        raise credentials_exception

    return sender


def get_auth_crew(
        token: str = Depends(crew_scheme),
        session: Session = Depends(create_session),
) -> Sender:
    try:
        crew_name = get_token_subject(token)
        if crew_name is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    crew = get_crew(session, crew_name)
    if crew is None:
        raise credentials_exception

    return crew
