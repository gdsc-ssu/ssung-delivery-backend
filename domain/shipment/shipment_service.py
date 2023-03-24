import re
from typing import Optional
from enum import Enum

from sqlalchemy.orm import Session

from domain.common.identifier import create_identifier
from domain.crew.crew_query import select_crew
from domain.shipment.shipment_query import select_shipment, insert_shipment, select_all_shipments
from domain.shipment.shipment_schema import ShipmentIn, ShipmentOut, ShipmentCreateOk
from models import Sender, Shipment


def convert_to_shipment(session: Session, schema: ShipmentIn, sender: Sender) -> Shipment:
    return Shipment(
        crew_id=select_crew(session, "string").id,  # TODO: replace stub
        sender_id=sender.id,
        destination=schema.destination,
        receiver_name=schema.receiver_name,
        receiver_phone_number=schema.receiver_phone_number,
        content=schema.content,
        shipment_detail=schema.shipment_detail,
        identifier=create_identifier(session),
    )


class OutSchema(Enum):
    def __call__(self):
        return self.value

    def __contains__(self, member) -> bool:
        return member in self.value.__fields__

    OUT = ShipmentOut
    CREATEOK = ShipmentCreateOk


def __convert(shipment_info: dict, schema: OutSchema) -> ShipmentOut | ShipmentCreateOk:
    """
    딕셔너리를 출력 데이터 모델로 변환 합니다.
    Args:
        shipment_info (dict): 배송 정보가 저장된 딕셔너리
        res (OutSchema): 출력하고 싶은 데이터 모델
    Returns:
        ShipmentOut: 배송정보 출력 모델
    """
    result = schema()

    # 불필요한 key들은 제거하고 출력 모델에 존재하는 key만 추출한다
    shipment_out_info = {col: val for col, val in shipment_info.items() if col in schema}
    return result(**shipment_out_info)


def convert_to_shipment_out(shipment_info: dict) -> ShipmentOut:
    return __convert(shipment_info, OutSchema.OUT)


def convert_to_shipment_create_ok(shipment_info: dict) -> ShipmentCreateOk:
    return __convert(shipment_info, OutSchema.CREATEOK)


def create_shipment(
    session: Session,
    orders: ShipmentIn | list[ShipmentIn],
    sender: Sender,
) -> ShipmentCreateOk | list[ShipmentCreateOk]:
    """
    배송 주문 생성을 위한 함수 입니다.
    Args:
        session: DB 연결을 위한 세션
        orders: 배송 추가를 위한 스키마
        sender: 발송자 엔티티
    """
    # print(sender.id, sender.sender_name)
    if isinstance(orders, list):
        result = []
        converted_orders = [convert_to_shipment(session, order, sender) for order in orders]

        for order in converted_orders:
            insert_shipment(session, order)
            result.append(convert_to_shipment_create_ok(order.as_dict))

    else:
        order = convert_to_shipment(session, orders, sender)
        insert_shipment(session, order)
        result = convert_to_shipment_create_ok(order.as_dict)

    return result


def masking(shipment: Shipment) -> dict:
    """
    부분 정보 제공을 위한 마스킹을 실시합니다

    Args:
        shipment (Shipment): 배송 정보

    Returns:
        dict: ShipmentOut에 사용되는 기본 정보
        {
            receiver_name: 성을 마스킹 처리
            receiver_phone_number: 핸드폰 뒤의 4자리 마스킹 처리
            destination: 상세 주소 전부 마스킹 처리
        }
    """

    # 수신자 이름으로 유저 신원 파악
    # 일치하지 않는 경우 마스킹한 정보를 전송한다.
    masked_info = {
        "receiver_name": re.sub(r"[가-힣]{2}$", "**", shipment.receiver_name or ""),
        "receiver_phone_number": re.sub(r"\d{4}$", "****", shipment.receiver_phone_number or ""),
        "destination": " ".join(shipment.destination.split()[:2]),  # 마스킹 처리하지 말고 부분 정보만 넘겨주기
    }
    masked_info["identifier"] = shipment.identifier
    return masked_info


def read_shipment(
    shipment_id: int,
    receiver_name: Optional[str],
    receiver_phone_number: Optional[str],
    session: Session,
) -> ShipmentOut:
    """
    배송 주문 정보를 가져 오기 위한 함수 입니다. 수신자 이름의 존재 여부로 데이터의 마스킹 여부를 판단합니다.
    Args:
        session: DB 연결을 위한 세션
        receiver_name: 수신자 이름. 마스킹 처리 여부를 판단하기 위해 사용됩니다.
        receiver_phone_number: 수신자의 전화번호
        shipment_id: 주문 데이터를 조회하기 위한 주문 번호

    Returns:
        ShipmentOut: 배송 정보 DTO
    """
    try:
        # 주문번호 기반으로 조회 TODO 식별자 사용 조회
        shipment = select_shipment(session, shipment_id)
        shipment_info = shipment._asdict()

        # 전화번호 추가 검증
        if (
            receiver_name != shipment.receiver_name
            or receiver_phone_number != shipment.receiver_phone_number
        ):
            shipment_info = masking(shipment)

        return convert_to_shipment_out(shipment_info)

    except Exception as e:
        raise e


def read_all_shipment(
    sender: Sender,
    session: Session,
) -> list[ShipmentOut]:
    try:
        shipments = select_all_shipments(session, sender)
        return [convert_to_shipment_out(shipment._asdict()) for shipment in shipments]

    except Exception as e:
        raise e
