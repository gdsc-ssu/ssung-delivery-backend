from fastapi import APIRouter, Header, Depends, HTTPException
from starlette import status

from database import create_session
from domain.shipment import shipment_schema, shipment_crud

router = APIRouter(prefix="/api/shipment")


@router.post("/order", status_code=status.HTTP_201_CREATED, tags=['shipments'])
def shipping_order(
        shipment_in: shipment_schema.ShipmentIn | list[shipment_schema.ShipmentIn],
        session=Depends(create_session),
        access_token: str = Header(convert_underscores=False)
):
    try:
        shipment_crud.create_shipment(
            session=session,
            orders=shipment_in,
            access_token=access_token
        )

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/cancel", status_code=status.HTTP_204_NO_CONTENT, tags=['shipments'])
def shipping_order():
    return "DEVELOPING...."  # TODO: 배송 취소 라우터 구현


@router.get("/track", status_code=status.HTTP_200_OK, tags=['shipments'])
def shipping_tracking():
    return "DEVELOPING...."  # TODO: 배송 조회 라우터 구현
