from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from authentication import get_current_sender
from database import create_session
from domain.shipment import shipment_schema, shipment_crud
from domain.shipment.shipment_crud import delete_shipment
from models import Sender

router = APIRouter(prefix="/api/shipment")


@router.post("/order", status_code=status.HTTP_201_CREATED, tags=['shipments'])
def shipping_order(
        shipment_in: shipment_schema.ShipmentIn | list[shipment_schema.ShipmentIn],
        session: Session = Depends(create_session),
        sender: Sender = Depends(get_current_sender)
):
    try:
        shipment_crud.create_shipment(session=session, orders=shipment_in, sender=sender)
        return {"ok": True}

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/cancel/{shipment_id}", tags=['shipments'])
def shipping_order(
        shipment_id: int,
        session: Session = Depends(create_session),
        sender: Sender = Depends(get_current_sender)
):
    try:
        delete_shipment(session, sender, shipment_id)
        return {"ok": True}

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/track", status_code=status.HTTP_200_OK, tags=['shipments'])
def shipping_tracking():
    return "DEVELOPING...."  # TODO: 배송 조회 라우터 구현
