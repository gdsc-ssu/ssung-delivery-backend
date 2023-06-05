import datetime
import enum

from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, BIGINT, Enum, ForeignKey
from sqlalchemy.sql.expression import func

from database import Base, engine
from utils import decode_id

status_default = {
    "date": datetime.datetime.now().strftime("%Y:%m:%d:%H:%M"),
    "location": "Seoul",
    "status": 0,
}

class Status(enum.Enum):
    ordered = 0
    shipping = 1
    out_for_delivery = 2
    shipped = 3


class Sender(Base):
    __tablename__ = "senders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(String(30), nullable=False, unique=True)
    sender_name = Column(String(30), nullable=False)
    password = Column(String(200), nullable=False)
    address = Column(String(50), nullable=False)
    sender_phone_number = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now())

    def __repr__(self) -> str:
        return f"<Sender id={self.id}, sender_id={self.sender_id}>"


class Crew(Base):
    __tablename__ = "crews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    crew_id = Column(String(30), nullable=False, unique=True)
    crew_name = Column(String(30), nullable=False)
    password = Column(String(200), nullable=False)
    area = Column(String(50), nullable=False)
    crew_phone_number = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    def __repr__(self) -> str:
        return f"<Crew id={self.id}, crew_id={self.crew_id}>"


# class Content(Base):
#     __tablename__ = 'contents'
#     id = Column(BIGINT, primary_key=True, autoincrement=True)
#     name = Column(String(255), nullable=False)
#     type = Column(String(255), nullable=False)
#     fragile = Column(Boolean, default=false)
#     express = Column(Boolean, default=false)
#     created_at = Column(TIMESTAMP, default=func.now())
#     updated_at = Column(TIMESTAMP, default=func.now())


class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    crew_id = Column(Integer, ForeignKey("crews.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("senders.id"), nullable=False)
    status = Column(Enum(Status), default=Status.ordered)
    content = Column(String(100), nullable=False)
    shipment_detail = Column(String(255), nullable=True)  # 배송시 주의사항 등
    destination = Column(String(255), nullable=False)
    receiver_name = Column(String(255), nullable=True)
    receiver_phone_number = Column(String(255), nullable=True)
    shipment_start_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    shipment_end_date = Column(TIMESTAMP, nullable=True)
    identifier = Column(String(255), unique=True)
    history = Column(
        JSON,
        default=[status_default],
    )

    def __repr__(self):
        return f"<Shipment id={self.id}, identifier={decode_id(self.identifier)}>"

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # content_id = Column(BIGINT, ForeignKey("contents.id"), nullable=False)
    # location = Column(String(255), nullable=False)

    # shipment_start_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    # shipment_end_date = Column(TIMESTAMP)


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(255), nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
# session = create_session()
# print(next(session).query(Shipment).all())
