from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from authentication import get_auth_sender, get_auth_crew
from database import create_session
from domain.common.router import exception_handler
from domain.shipment import shipment_schema, shipment_service
from domain.shipment.shipment_query import delete_shipment
from domain.shipment.shipment_schema import ShipmentOut, ShipmentCreateOk, ShipmentPatch
from models import Sender, Crew

router = APIRouter(prefix="/shipment", tags=["shipments"])


@exception_handler
@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=ShipmentCreateOk | list[ShipmentCreateOk],
)
def create(
    shipment_in: shipment_schema.ShipmentIn | list[shipment_schema.ShipmentIn],
    session: Session = Depends(create_session),
    sender: Sender = Depends(get_auth_sender),
):
    return shipment_service.create_shipment(session=session, orders=shipment_in, sender=sender)


@exception_handler
@router.delete("/delete/{shipment_id}")
async def delete(
    shipment_id: int,
    session: Session = Depends(create_session),
    sender: Sender = Depends(get_auth_sender),
):
    return delete_shipment(session, sender, shipment_id)


@exception_handler
@router.get("/read/{shipment_id}", status_code=status.HTTP_200_OK, response_model=ShipmentOut)
async def read(
        shipment_id: int | str,
        receiver_name: Optional[str] = None,
        receiver_phone_number: Optional[str] = None,
        session: Session = Depends(create_session),
) -> ShipmentOut:
    """
    배송 번호를 통해 배송 정보를 조회하는 api입니다.
    수신자 이름을 통해 유저 익명의 유저를 확인하며 수신자 이름이 일치할 경우 정보를 전부 제공합니다.
    일치하지 않을 경우 마스킹 된 부분 정보를 제공합니다.

    Args:
        shipment_id (str): 배송 번호
        receiver_name (str, optional): 수신자 이름. Defaults to None.
        receiver_phone_number: 수신자의 전화번호
        session (Session): 디비 연결을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 조회하려는 배송정보가 존재하지 않는 경우

    Returns:
        ShipmentOut: 기본적인 배송 정보가 담겨 있다.
    """
    return shipment_service.read_shipment(
        shipment_id, receiver_name, receiver_phone_number, session
    )


@exception_handler
@router.get("/read-all", status_code=status.HTTP_200_OK)
async def read_all(
        sender: Sender = Depends(get_auth_sender), session: Session = Depends(create_session)
) -> list[ShipmentOut]:
    return shipment_service.read_all_shipment(sender, session)


@exception_handler
@router.patch("/update/{shipment_id}")
async def update(
        shipment_id: int,
        shipment_patch: ShipmentPatch,
        session: Session = Depends(create_session),
        crew: Crew = Depends(get_auth_crew)
) -> ShipmentOut:
    return shipment_service.update_shipment(shipment_id, crew, shipment_patch, session)


@exception_handler
@router.get("/track", status_code=status.HTTP_200_OK)
async def shipping_tracking():
    return "DEVELOPING...."  # TODO: 배송 조회 라우터 구현
