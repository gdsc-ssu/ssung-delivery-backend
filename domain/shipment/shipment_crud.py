from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from domain.crew import crew_crud
from domain.sender import sender_crud
from domain.shipment import shipment_schema
from models import Shipment
from utils import get_token_subject


def convert_to_model(
        session: Session,
        schema: shipment_schema.ShipmentIn,
        access_token: str
) -> Shipment:
    return Shipment(
        content_id=1,  # TODO: replace stub
        crew_id=crew_crud.get_crew(session, "string").id,  # TODO: replace stub
        sender_id=sender_crud.get_sender(
            session, get_token_subject(access_token)
        ).id,
        location="location",  # TODO: replace stub
        destination=schema.destination,
        receiver_name=schema.receiver_name,
        receiver_phone_number=schema.receiver_phone_number,
        shipment_detail=schema.shipment_detail
    )


def create_shipment(
        session: Session,
        orders: shipment_schema.ShipmentIn | list[shipment_schema.ShipmentIn],
        access_token: str
) -> None:
    """
    배송 주문 생성을 위한 함수 입니다.
    Args:
        session: DB 연결을 위한 세션
        orders: 배송 추가를 위한 스키마
        access_token: 발송자 인증을 위한 토큰
    """

    if isinstance(orders, list):
        converted_orders = [
            convert_to_model(session, order, access_token)
            for order in orders
        ]

        for order in converted_orders:
            session.add(order)

    else:
        session.add(convert_to_model(session, orders, access_token))


def delete_shipment(
        session: Session,
        access_token: str,
        shipment_id: int
):
    try:
        query = session.query(Shipment).filter(Shipment.id == shipment_id).first()
        sender = sender_crud.get_sender(session, get_token_subject(access_token))

        if query is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if query.sender_id != sender.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        session.delete(query)

    except Exception as e:
        raise e
