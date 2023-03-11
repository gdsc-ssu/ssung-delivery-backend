from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from database import create_session
from domain.common.router import exception_handler
from domain.crew import crew_schema
from domain.crew.crew_service import create_crew, login_crew

router = APIRouter(prefix="/crew")  # url 라우팅


@exception_handler
@router.post("/create", status_code=status.HTTP_201_CREATED, tags=["crews"])
def create(
        crew_in: crew_schema.CrewIn,
        session: Session = Depends(create_session)
) -> dict:
    """
    유저를 생성 합니다.

    Args:
        crew_in (CrewIn): 유저 생성을 위한 입력 형태 (유저 이름, 비밀 번호, 주소, 핸드폰 번호)
        session (Session, optional): DB 연결을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 409에러 이미 유저가 존재
    """
    return create_crew(crew_in, session)


@exception_handler
@router.post("/login", response_model=crew_schema.CrewOut, tags=["crews"])
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(create_session)
) -> dict:
    """
    로그인 토큰을 검증해 로그인을 진행 합니다.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): fastapi 제공 토큰 제공 폼 타입. Defaults to Depends().
        session (Session, optional): DB 연결을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 401 로그인 에러
        HTTPException: 500 서버 에러

    Returns:
        crew_out: crew 출력 모델
    """
    return login_crew(form_data, session)
