from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from database import create_session
from domain.crew import crew_crud
from domain.crew import crew_schema
from utils import verify_password, create_access_token

router = APIRouter(prefix="/api/crew")  # url 라우팅


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT, tags=["crews"])
def crew_create(crew_in: crew_schema.CrewIn, session=Depends(create_session)):
    """
    유저를 생성 합니다.

    Args:
        crew_in (CrewIn): 유저 생성을 위한 입력 형태 (유저 이름, 비밀 번호, 주소, 핸드폰 번호)
        session (Session, optional): DB 연결을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 409에러 이미 유저가 존재
    """
    try:
        crew = crew_crud.get_crew(session, crew_in.crew_name)
        if crew:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Crew already Exists.")

        crew_crud.create_crew(session=session, crew_in=crew_in)

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/login", response_model=crew_schema.CrewOut, tags=["crews"])
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
        crewout: crew 출력 모델
    """
    try:
        crew = crew_crud.get_crew(session, form_data.username)
        if crew and verify_password(form_data.password, crew.password):
            access_token = create_access_token(subject=crew.crew_name)
            return {"access_token": access_token,
                    "token_type": "bearer",
                    "crewname": crew.crew_name
                    }
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect crewname or password")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
