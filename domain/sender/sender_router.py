from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from database import create_session
from domain.common.router import exception_handler
from domain.sender import sender_schema
from domain.sender.sender_service import create_sender, login_sender

router = APIRouter(prefix="/sender", tags=["senders"])  # url 라우팅


@exception_handler
@router.post("/create", status_code=status.HTTP_201_CREATED)
def create(
        sender_in: sender_schema.SenderIn,
        session: Session = Depends(create_session)
) -> dict:
    """
        유저를 생성합니다.

        Args:
            sender_in (sender_schema.SenderIn): 유저 생성을 위한 입력 형태 (유저 이름, 비밀번호, 주소, 핸드폰 번호)
            session (Session, optional): DB 커넥션을 위한 세션. Defaults to Depends(create_session).

        Raises:
            HTTPException: 409에러 이미 유저가 존재
    """
    return create_sender(session, sender_in)


@exception_handler
@router.post("/login", response_model=sender_schema.SenderOut)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(create_session)
):
    """
        로그인 토큰을 검증해 로그인을 진행 합니다.

        Args:
            form_data (OAuth2PasswordRequestForm, optional): fastapi 제공 토큰 제공 폼 타입. Defaults to Depends().
            session (Session, optional): DB 연결을 위한 세션. Defaults to Depends(create_session).

        Raises:
            HTTPException: 401 로그인 에러
            HTTPException: 500 서버 에러

        Returns:
            SenderOut: Sender 출력 모델
    """
    return login_sender(session, form_data)
