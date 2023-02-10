from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.expression import func

from database import *


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(30), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    address = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())


class Crew(Base):
    __tablename__ = 'crews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    crew_name = Column(String(30), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    area = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())

# if __name__ == '__main__':
#     Base.metadata.create_all(engine)
