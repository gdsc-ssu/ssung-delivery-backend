from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from domain.crew import crew_crud
from domain.shipment import shipment_schema
from models import Shipment, Sender


def convert_to_model(
        session: Session,
        schema: shipment_schema.ShipmentIn,
        sender: Sender
) -> Shipment:
    return Shipment(
        content_id=1,  # TODO: replace stub
        crew_id=crew_crud.get_crew(session, "string").id,  # TODO: replace stub
        sender_id=sender.id,
        location="location",  # TODO: replace stub
        destination=schema.destination,
        receiver_name=schema.receiver_name,
        receiver_phone_number=schema.receiver_phone_number,
        shipment_detail=schema.shipment_detail
    )


def create_shipment(
        session: Session,
        orders: shipment_schema.ShipmentIn | list[shipment_schema.ShipmentIn],
        sender: Sender
) -> None:
    """
    배송 주문 생성을 위한 함수 입니다.
    Args:
        session: DB 연결을 위한 세션
        orders: 배송 추가를 위한 스키마
        sender: 발송자 엔티티
    """

    if isinstance(orders, list):
        converted_orders = [
            convert_to_model(session, order, sender)
            for order in orders
        ]

        for order in converted_orders:
            session.add(order)

    else:
        session.add(convert_to_model(session, orders, sender))


def delete_shipment(
        session: Session,
        sender: Sender,
        shipment_id: int
) -> None:
    """
    배송 주문을 삭제 하는 함수 입니다.
    Args:
        session: DB 연결을 위한 세션
        sender: 발송자 인증을 위한 토큰
        shipment_id: 삭제 하려고 하는 주문 ID
    """
    try:
        query = session.query(Shipment).filter(Shipment.id == shipment_id).first()

        if query is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if query.sender_id != sender.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        session.delete(query)

    except Exception as e:
        raise e
