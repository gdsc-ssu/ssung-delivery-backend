from utils import get_hash_password
from sqlalchemy.orm import Session
from models import Crew
from domain.crew import crew_schema
from typing import Union


def create_crew(session:Session, crew_in:crew_schema.CrewIn) -> None:
    """
    크루 생성을 위한 함수입니다. 크루를 생성해 DB에 추가합니다.

    Args:
        session (Session): DB연결을 위한 세션
        Crew_in (Crew_schema.CrewIn): 크루 입력을 위한 검증 스키마
    """
    crew = Crew(crew_name=crew_in.crew_name, password=get_hash_password(crew_in.password), \
                area=crew_in.area, phone_number=crew_in.phone_number)

    session.add(crew) #DB에 유처 정보를 추가합니다.


def get_crew(session:Session, crew_name:str) -> Union[Crew, None]:
    """
    크루 이름을 기반으로 DB에서 크루 정보를 선택합니다.

    Args:
        session (Session): DB연결 세션입니다.
        Crew_name (str): DB에 저장된 크루 이름

    Returns:
        Crew, None: DB에 크루 이름을 기반으로 탐색한 결과를 반환합니다. 결과는 row이거나 None입니다.
    """
    query = session.query(Crew).filter(Crew.crew_name==crew_name).first()
    
    return query

