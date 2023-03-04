from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from authentication import get_auth_sender
from database import create_session
from domain.shipment import shipment_schema, shipment_crud
from domain.shipment.shipment_crud import delete_shipment, select_shipment, select_sender_shipments
from models import Sender

router = APIRouter(prefix="/api/shipment")


@router.post("/order", status_code=status.HTTP_201_CREATED, tags=['shipments'])
async def shipping_order(
        shipment_in: shipment_schema.ShipmentIn | list[shipment_schema.ShipmentIn],
        session: Session = Depends(create_session),
        sender: Sender = Depends(get_auth_sender)
):
    try:
        shipment_crud.create_shipment(session=session, orders=shipment_in, sender=sender)
        return {"ok": True}

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/cancel/{shipment_id}", tags=['shipments'])
async def shipping_order(
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


@router.get("/show", status_code=status.HTTP_200_OK, tags=['shipments'], response_model=shipment_schema.ShipmentOut)
async def show_shipmnet(shipemnt_id:str, receiver_name:str=None, session:Session=Depends(create_session)):
    """
    배송 번호를 통해 배송 정보를 조회하는 api입니다. 
    수신자 이름을 통해 유저 익명의 유저를 확인하며 수신자 이름이 일치할 경우 정보를 전부 제공합니다.
    일치하지 않을 경우 마스킹 된 부분 정보를 제공합니다.

    Args:
        shipemnt_id (str): 배송 번호
        receiver_name (str, optional): 수신자 이름. Defaults to None.
        session (Session, optional): 디비 연결을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 조회하려는 배송정보가 존재하지 않는 경우

    Returns:
        ShipmentOut: 기본적인 배송 정보가 담겨 있다.
    """
    shipment = select_shipment(session, shipemnt_id) #주문번호 기반으로 조회 TODO 식별자 사용 조회
    if shipment:
        if shipment.receiver_name != receiver_name: #수신자 이름으로 유저 신원 파악
            shipment_info = shipment_crud.mask_shipment(shipment) #일치하지 않는 경우 마스킹한 정보를 전송한다.
        else:
            #일치할 경우 마스킹 되지 않은 정보를 활용한다.
            shipment_info =  {"receiver_name":shipment.receiver_name, "receiver_phone_number":shipment.receiver_phone_number, "destination": shipment.destination}
        
        return shipment_schema.ShipmentOut(**shipment_info)
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/sender_shipments", status_code=status.HTTP_200_OK, tags=['shipments'])
async def show_sender_shipments(sender:Sender=Depends(get_auth_sender), session:Session=Depends(create_session)):
    print(sender.__dict__)
    shipments = select_sender_shipments(session, sender.id)
    if shipments:
        return shipments
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

