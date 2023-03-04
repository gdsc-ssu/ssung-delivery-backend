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


def mask_name(name:str) -> str:
    return "*" + name[1:] #성 마스킹


def mask_phone_num(phone_number:str) -> str:
    num_list = phone_number.split("-")
    num_list[-1] = "****" #끝에 4자리 마스킹
    return '-'.join(num_list)


def mask_destination(destination:str) -> str:
    det_list = destination.split()
    do_mask = lambda x: len(x) * "*"
    maksed_address= [do_mask(address) for address in det_list]
    return ' '.join(det_list[:2] + (maksed_address)) #상세 주소 전부 마스킹 처리
    

def mask_shipment(shipment:Shipment) -> dict:
    """
    부분 정보 제공을 위한 마스킹을 실시합니다

    Args:
        shipment (Shipment): 배송 정보

    Returns:
        dict: ShipmentOut에 사용되는 기본 정보
    """
    receiver_name = mask_name(shipment.receiver_name) #성을 마스킹 처리
    receiver_phone_number = mask_phone_num(shipment.receiver_phone_number) #핸드폰 뒤의 4자리 마스킹 처리
    destination = mask_destination(shipment.destination) #시 동 구 까지만 출력되게 
    return {"receiver_name":receiver_name, "receiver_phone_number":receiver_phone_number, "destination": destination}


def select_shipment(
        session: Session,
        shipment_id:str,
    ) -> Shipment:
    """
    배송 테이블에서 뱌송 번호를 기반으로 테이블을 조회합니다.

    Args:
        session (Session): 연결 세션
        shipment_id (str): 배송 번호

    Returns:
        Shipment: 배송 정보
    """

    shipment = session.query(Shipment).filter_by(id=shipment_id).first()
    return shipment


def select_sender_shipments(session:Session, sender_id:int) -> list:
    shipemnts = session.query(Shipment).filter_by(sender_id=sender_id).all()
    return shipemnts