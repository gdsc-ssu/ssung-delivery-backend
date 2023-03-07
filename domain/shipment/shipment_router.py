import sys
import traceback
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from authentication import get_auth_sender
from database import create_session
from domain.shipment import shipment_schema, shipment_service
from domain.shipment.shipment_query import delete_shipment
from domain.shipment.shipment_schema import ShipmentOut
from models import Sender

router = APIRouter(prefix="/api/shipment")


@router.post("/create", status_code=status.HTTP_201_CREATED, tags=['shipments'])
async def create(
        shipment_in: shipment_schema.ShipmentIn | list[shipment_schema.ShipmentIn],
        session: Session = Depends(create_session),
        sender: Sender = Depends(get_auth_sender)
):
    try:
        shipment_service.create_shipment(session=session, orders=shipment_in, sender=sender)
        return {"ok": True}

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/delete/{shipment_id}", tags=['shipments'])
async def delete(
        shipment_id: int,
        session: Session = Depends(create_session),
        sender: Sender = Depends(get_auth_sender)
):
    try:
        delete_shipment(session, sender, shipment_id)
        return {"ok": True}

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/track", status_code=status.HTTP_200_OK, tags=['shipments'])
async def shipping_tracking():
    return "DEVELOPING...."  # TODO: 배송 조회 라우터 구현


@router.get("/read/{shipment_id}", status_code=status.HTTP_200_OK, tags=['shipments'], response_model=ShipmentOut)
async def read(
        shipment_id: int,
        receiver_name: Optional[str] = None,
        session: Session = Depends(create_session)
) -> ShipmentOut:
    """
    배송 번호를 통해 배송 정보를 조회하는 api입니다. 
    수신자 이름을 통해 유저 익명의 유저를 확인하며 수신자 이름이 일치할 경우 정보를 전부 제공합니다.
    일치하지 않을 경우 마스킹 된 부분 정보를 제공합니다.

    Args:
        shipment_id (str): 배송 번호
        receiver_name (str, optional): 수신자 이름. Defaults to None.
        session (Session): 디비 연결을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 조회하려는 배송정보가 존재하지 않는 경우

    Returns:
        ShipmentOut: 기본적인 배송 정보가 담겨 있다.
    """
    try:
        return shipment_service.read_shipment(shipment_id, receiver_name, session)

    except HTTPException as e:
        raise e

    except Exception as e:
        traceback.print_exception(*sys.exc_info())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
