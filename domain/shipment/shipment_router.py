from fastapi import APIRouter, Header, Depends, HTTPException
from starlette import status

from database import create_session
from domain.shipment import shipment_schema, shipment_crud
from domain.shipment.shipment_crud import delete_shipment, convert_to_model

router = APIRouter(prefix="/api/shipment")


@router.post("/order", status_code=status.HTTP_201_CREATED, tags=['shipments'])
def shipping_order(
        shipment_in: shipment_schema.ShipmentIn | list[shipment_schema.ShipmentIn],
        session=Depends(create_session),
        access_token: str | None = Header(convert_underscores=False, default=None)
):
    try:
        if access_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        shipment_crud.create_shipment(
            session=session,
            orders=shipment_in,
            access_token=access_token
        )

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/cancel/{shipment_id}", tags=['shipments'])
def shipping_order(
        shipment_id: int,
        session=Depends(create_session),
        access_token: str | None = Header(convert_underscores=False, default=None)
):
    try:
        if access_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        delete_shipment(session, access_token, shipment_id)
        return {"ok": True}

    except HTTPException as e:
        raise e

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/track", status_code=status.HTTP_200_OK, tags=['shipments'])
def shipping_tracking():
    return "DEVELOPING...."  # TODO: 배송 조회 라우터 구현
