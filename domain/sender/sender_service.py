from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from domain.sender import sender_query
from domain.sender.sender_schema import SenderIn
from utils import verify_password, create_access_token


def create_sender(session: Session, sender_in: SenderIn) -> dict:
    """
    Sender를 생성하는 서비스 입니다.

    Args:
        session (Session, optional): DB 연결을 위한 세션. Defaults to Depends(create_session).
        sender_in (sender_schema.SenderIn): 유저 생성을 위한 입력 형태 (유저 이름, 비밀번호, 주소, 핸드폰 번호)

    Raises:
        HTTPException: 409 유저가 이미 존재 합니다.

    Returns:
        dict {"ok": True}
    """
    try:
        sender = sender_query.select_sender(session, sender_in.sender_id)

        if sender:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Same Id already Exists."
            )

        sender_query.insert_sender(session=session, sender_in=sender_in)
        return {"ok": True}

    except Exception as e:
        raise e


def login_sender(session: Session, form_data: OAuth2PasswordRequestForm):
    """
    Sender의 AccessToken을 제공받기 위해 사용합니다.

    Args:
        session (Session, optional): DB 연결을 위한 세션. Defaults to Depends(create_session).
        form_data (OAuth2PasswordRequestForm, optional): fastapi 제공 토큰 제공 폼 타입. Defaults to Depends().

    Raises:
        HTTPException: 401 sender_name 또는 password가 정확하지 않습니다.

    Returns:
        dict
        {
            "access_token": 액세스 토큰,
            "token_type": "bearer",
            "sender_name": sender_name
        }
    """
    try:
        sender = sender_query.select_sender(session, form_data.username)

        if sender is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if not verify_password(form_data.password, sender.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect sender_name or password"
            )

        access_token = create_access_token(subject=sender.sender_id)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "sender_name": sender.sender_name,
        }

    except Exception as e:
        raise e
