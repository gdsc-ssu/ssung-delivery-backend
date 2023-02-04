from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:kidok0714@localhost:3306/ssung"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_session():
    """
    DB연결을 위한 세션을 생성한다.
    fastapi의존성을 위해 사용하며 모든 api는 이 함수의 내부에서 동작한다.

    Raises:
        e: DB 트랜젝션 중 에러가 발생하면 해당 세션에서 발생한 쿼리를 전부 롤백한다.

    Yields:
        generator: 세션 제너레이터
    """
    session = Session()
    try:
        yield session

    except Exception as e:
        session.rollback() #트랜젝션 되돌림
        raise e
    
    else:
        session.commit()
    
    finally:
        session.close()
