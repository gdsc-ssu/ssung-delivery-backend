from typing import List

from sqlalchemy.orm import Session

from domain.crew import crew_crud
from domain.sender import sender_crud
from domain.shipment import shipment_schema
from models import Shipment
from utils import get_token_subject


def create_shipment(
        session: Session,
        requested_orders: List[shipment_schema.ShipmentIn],
        access_token: str
) -> None:
    """
    배송 주문 생성을 위한 함수 입니다.
    Args:
        session: DB 연결을 위한 세션
        requested_orders: 배송 추가를 위한 스키마
        access_token: 발송자 인증을 위한 토큰
    """

    converted_orders = [
        Shipment(
            content_id=1,  # TODO: replace stub
            crew_id=crew_crud.get_crew(session, "string"),  # TODO: replace stub
            sender_id=sender_crud.get_sender(
                session, get_token_subject(access_token)
            ),
            location="location",  # TODO: replace stub
            destination=order.destination,
            receiver_name=order.receiver_name,
            receiver_phone_number=order.receiver_phone_number,
            shipment_detail=order.shipment_detail
        ) for order in requested_orders
    ]

    for order in converted_orders:
        session.add(order)