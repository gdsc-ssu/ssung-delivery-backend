from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

DATABASE_URL = "mysql+pymysql://root:kidok0714@localhost:3306/ssung"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_session():
    Session = sessionmaker(bind=engine)
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
