from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from domain.crew import crew_query, crew_schema
from utils import verify_password, create_access_token


def create_crew(crew_in: crew_schema.CrewIn, session: Session) -> dict:
    """
    Crew를 생성하는 서비스 입니다.

    Args:
        crew_in (crew_schema.CrewIn): 유저 생성을 위한 입력 형태 (유저 이름, 비밀번호, 주소, 핸드폰 번호)
        session (Session, optional): DB 연결을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 409 유저가 이미 존재 합니다.

    Returns:
        dict {"ok": True}
    """
    try:
        crew = crew_query.select_crew(session, crew_in.crew_name)

        if crew:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Crew already Exists.")

        crew_query.insert_crew(session=session, crew_in=crew_in)
        return {"ok": True}

    except Exception as e:
        raise e


def login_crew(form_data: OAuth2PasswordRequestForm, session: Session) -> dict:
    """
    Crew의 AccessToken을 제공받기 위해 사용합니다.

    Args:
        session (Session, optional): DB 연결을 위한 세션. Defaults to Depends(create_session).
        form_data (OAuth2PasswordRequestForm, optional): fastapi 제공 토큰 제공 폼 타입. Defaults to Depends().

    Raises:
        HTTPException: 401 crew_name 또는 password가 정확하지 않습니다.

    Returns:
        dict
        {
            "access_token": 액세스 토큰,
            "token_type": "bearer",
            "crew_name": crew_name
        }
    """
    try:
        crew = crew_query.select_crew(session, form_data.username)

        if crew is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if not verify_password(form_data.password, crew.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect crewname or password"
            )

        access_token = create_access_token(subject=crew.crew_name)
        return {"access_token": access_token, "token_type": "bearer", "crew_name": crew.crew_name}

    except Exception as e:
        raise e
