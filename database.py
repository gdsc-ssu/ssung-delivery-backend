from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from config import settings

engine = create_engine(settings.DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_session() -> Iterable[Session]:
    """
    DB 연결을 위한 세션을 생성 한다.
    fastapi 의존성을 위해 사용 하며 모든 api는 이 함수의 내부 에서 동작 한다.

    Raises:
        e: DB 트랜젝션 중 에러가 발생 하면 해당 세션 에서 발생한 쿼리를 전부 롤백 한다.

    Yields:
        generator: 세션 제너레이터
    """
    session = Session()
    try:
        yield session

    except Exception as e:
        session.rollback()
        raise e

    else:
        session.commit()

    finally:
        session.close()
