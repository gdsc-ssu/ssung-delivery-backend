from fastapi import HTTPException
from sqlalchemy.orm import Session, Query
from starlette import status

from domain.common.query import transactional
from models import Shipment, Sender, Crew


@transactional
def insert_shipment(session: Session, order: Shipment) -> None:
    """
    배송 주문 생성을 위한 함수 입니다.
    Args:
        session: DB 연결을 위한 세션
        order: 배송 추가를 위한 스키마
    """
    session.add(order)


@transactional
def delete_shipment(session: Session, sender: Sender, shipment_id: int) -> None:
    """
    배송 주문을 삭제 하는 함수 입니다.
    Args:
        session: DB 연결을 위한 세션
        sender: 발송자 인증을 위한 토큰
        shipment_id: 삭제 하려고 하는 주문 ID
    """
    query = session.query(Shipment).filter_by(id=shipment_id).first()

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if query.sender_id != sender.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    session.delete(query)


def create_read_query(session: Session) -> Query:
    query = (
        session.query(
            Shipment.identifier,
            Shipment.receiver_name,
            Shipment.content,
            Shipment.receiver_phone_number,
            Shipment.destination,
            Shipment.shipment_detail,
            Shipment.status,
            Shipment.history,
            Sender.sender_name,
            Sender.sender_phone_number,
            Crew.crew_name,
            Crew.crew_phone_number,
        )
        .join(Sender, Shipment.sender_id == Sender.id)
        .join(Crew, Shipment.crew_id == Crew.id)
    )
    return query


@transactional
def select_shipment(
    session: Session,
    shipment_id: int,
) -> tuple:
    """
    배송 테이블에서 뱌송 번호를 기반으로 테이블을 조회합니다.

    Args:
        session (Session): 연결 세션
        shipment_id (str): 배송 번호

    Returns:
        Shipment: 배송 정보
    """
    query = session.query(Shipment).filter_by(id=shipment_id).first()

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return query


@transactional
def select_all_shipments(session: Session, sender: Sender) -> list[Shipment]:
    query = session.query(Shipment).filter_by(sender_id=sender.id).all()

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return query
