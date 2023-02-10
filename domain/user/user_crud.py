from typing import Union

from sqlalchemy.orm import Session

from domain.user import user_schema
from models import User
from utils import get_hash_password


def create_user(session: Session, user_in: user_schema.UserIn) -> None:
    """
    유저 생성을 위한 함수 입니다. 유저를 생성해 DB에 추가 합니다.

    Args:
        session (Session): DB 연결을 위한 세션
        user_in (user_schema.UserIn): 유저 입력을 위한 검증 스키마
    """
    user = User(user_name=user_in.user_name, password=get_hash_password(user_in.password), \
                address=user_in.address, phone_number=user_in.phone_number)

    # session은 컨텍스트 매니저로 원자성 보존
    session.add(user)  # DB에 유처 정보를 추가 합니다.


def get_user(session: Session, user_name: str) -> Union[User, None]:
    """
    유저 이름을 기반 으로 DB에서 유저 정보를 선택 합니다.

    Args:
        session (Session): DB 연결 세션 입니다.
        user_name (str): DB에 저장된 유저 이름

    Returns:
        User, None: DB에 유저 이름을 기반 으로 탐색한 결과를 반환 합니다. 결과는 row 이거나 None 입니다.
    """
    query = session.query(User).filter(User.user_name == user_name).first()

    return query
