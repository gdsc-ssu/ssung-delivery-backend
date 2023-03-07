from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from domain.crew import crew_schema
from models import Crew
from utils import get_hash_password


def insert_crew(session: Session, crew_in: crew_schema.CrewIn) -> None:
    """
    크루 생성을 위한 함수 입니다. 크루를 생성해 DB에 추가 합니다.

    Args:
        session (Session): DB 연결을 위한 세션
        crew_in (Crew_schema.CrewIn): 크루 입력을 위한 검증 스키마
    """
    try:
        crew = Crew(
            crew_name=crew_in.crew_name,
            password=get_hash_password(crew_in.password),
            area=crew_in.area,
            phone_number=crew_in.phone_number
        )

        session.add(crew)  # DB에 유처 정보를 추가 합니다.

    except Exception as e:
        raise e


def select_crew(session: Session, crew_name: str) -> Crew:
    """
    크루 이름을 기반 으로 DB 에서 크루 정보를 선택 합니다.

    Args:
        session (Session): DB 연결 세션 입니다.
        crew_name (str): DB에 저장된 크루 이름

    Returns:
        Crew, None: DB에 크루 이름을 기반 으로 탐색한 결과를 반환 합니다. 결과는 row 이거나 None 입니다.
    """
    try:
        query = session.query(Crew).filter_by(crew_name=crew_name).first()

        if query is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return query

    except Exception as e:
        raise e
