import enum

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, BIGINT, Enum, ForeignKey, false
from sqlalchemy.sql.expression import func

from database import Base


class Status(enum.Enum):
    ready = 0
    ongoing = 1
    finished = 2


class Sender(Base):
    __tablename__ = 'senders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_name = Column(String(30), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    address = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    modified_at = Column(TIMESTAMP, default=func.now())


class Crew(Base):
    __tablename__ = 'crews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    crew_name = Column(String(30), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    area = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())


class Content(Base):
    __tablename__ = 'contents'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    fragile = Column(Boolean, default=false)
    express = Column(Boolean, default=false)
    created_at = Column(TIMESTAMP, default=func.now())
    modified_at = Column(TIMESTAMP, default=func.now())


class Shipment(Base):
    __tablename__ = 'shipments'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    content_id = Column(BIGINT, ForeignKey("contents.id"), nullable=False)
    crew_id = Column(Integer, ForeignKey("crews.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("senders.id"), nullable=False)
    status = Column(Enum(Status), default=Status.ready)
    location = Column(String(255), nullable=False)
    shipment_detail = Column(String(255), nullable=True)  # 배송시 주의사항 등
    destination = Column(String(255), nullable=False)
    receiver_name = Column(String(255), nullable=True)
    receiver_phone_number = Column(String(255), nullable=True)
    shipment_start_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    shipment_end_date = Column(TIMESTAMP)

# if __name__ == '__main__':
# Base.metadata.create_all(engine)
# session = create_session()
# print(next(session).query(Shipment).all())
