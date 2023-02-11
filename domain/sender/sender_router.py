from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from database import create_session
from domain.sender import sender_crud
from domain.sender import sender_schema
from utils import verify_password, create_access_token

router = APIRouter(prefix="/api/sender")  # url 라우팅


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def sender_create(sender_in: sender_schema.SenderIn, session=Depends(create_session)):
    """
    유저를 생성합니다.

    Args:
        sender_in (sender_schema.SenderIn): 유저 생성을 위한 입력 형태 (유저 이름, 비밀번호, 주소, 핸드폰 번호)
        session (Session, optional): DB 커넥션을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 409에러 이미 유저가 존재
    """
    try:
        sender = sender_crud.get_sender(session, sender_in.sender_name)
        if sender:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already Exists.")

        sender_crud.create_sender(session=session, sender_in=sender_in)

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/login", response_model=sender_schema.SenderOut, tags=["senders"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(create_session)):
    """
    로그인 토큰을 검증해 로그인을 진행 합니다.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): fastapi 제공 토큰 제공 폼 타입. Defaults to Depends().
        session (Session, optional): DB 연결을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 401 로그인 에러
        HTTPException: 500 서버 에러

    Returns:
        Userout: User 출력 모델
    """
    try:
        sender = sender_crud.get_sender(session, form_data.username)
        if sender and verify_password(form_data.password, sender.password):
            access_token = create_access_token(subject=sender.sender_name)
            return {"access_token": access_token,
                    "token_type": "bearer",
                    "sender_name": sender.sender_name
                    }
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect sender_name or password")

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
