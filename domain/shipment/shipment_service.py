import re
from typing import Optional

from sqlalchemy.orm import Session

from domain.crew import crew_query
from domain.shipment import shipment_schema
from domain.shipment.shipment_query import select_shipment, insert_shipment
from domain.shipment.shipment_schema import ShipmentOut
from models import Sender, Shipment


def convert_to_shipment(
        session: Session,
        schema: shipment_schema.ShipmentIn,
        sender: Sender
) -> Shipment:
    return Shipment(
        content_id=1,  # TODO: replace stub
        crew_id=crew_query.select_crew(session, "string").id,  # TODO: replace stub
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
) -> dict:
    """
    배송 주문 생성을 위한 함수 입니다.
    Args:
        session: DB 연결을 위한 세션
        orders: 배송 추가를 위한 스키마
        sender: 발송자 엔티티
    """

    if isinstance(orders, list):
        converted_orders = [
            convert_to_shipment(session, order, sender)
            for order in orders
        ]

        for order in converted_orders:
            insert_shipment(session, order)

    else:
        insert_shipment(session, convert_to_shipment(session, orders, sender))

    return {"ok": True}


def masking(shipment: Shipment, receiver_name: str) -> dict:
    """
    부분 정보 제공을 위한 마스킹을 실시합니다

    Args:
        receiver_name (str): 수신자 이름
        shipment (Shipment): 배송 정보

    Returns:
        dict: ShipmentOut에 사용되는 기본 정보
        {
            receiver_name: 성을 마스킹 처리
            receiver_phone_number: 핸드폰 뒤의 4자리 마스킹 처리
            destination: 상세 주소 전부 마스킹 처리
        }
    """
    shipment_info = {
        "receiver_name": shipment.receiver_name,
        "receiver_phone_number": shipment.receiver_phone_number,
        "destination": shipment.destination
    }

    # 수신자 이름으로 유저 신원 파악
    # 일치하지 않는 경우 마스킹한 정보를 전송한다.
    if receiver_name is None or shipment.receiver_name != receiver_name:
        shipment_info = {
            "receiver_name": re.sub(r'[가-힣]{2}$', '**', shipment.receiver_name or ""),
            "receiver_phone_number": re.sub(r'\d{3,4}-\d{4}$', '****-****', shipment.receiver_phone_number or ""),
            "destination": ' '.join(
                shipment.destination.split()[:2] +
                [len(address) * "*" for address in shipment.destination.split()]
            )
        }
    return shipment_info


def read_shipment(
        shipment_id: int,
        receiver_name: Optional[str],
        session: Session
) -> ShipmentOut:
    """
    배송 주문 정보를 가져 오기 위한 함수 입니다. 수신자 이름의 존재 여부로 데이터의 마스킹 여부를 판단합니다.
    Args:
        session: DB 연결을 위한 세션
        receiver_name: 수신자 이름. 마스킹 처리 여부를 판단하기 위해 사용됩니다.
        shipment_id: 주문 데이터를 조회하기 위한 주문 번호

    Returns:
        ShipmentOut: 배송 정보 DTO
    """
    try:
        # 주문번호 기반으로 조회 TODO 식별자 사용 조회
        shipment = select_shipment(session, shipment_id)
        return ShipmentOut(**masking(shipment, receiver_name))

    except Exception as e:
        raise e
