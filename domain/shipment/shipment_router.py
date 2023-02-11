from fastapi import APIRouter
from starlette import status

router = APIRouter(prefix="/api/shipment")


@router.post("/order", status_code=status.HTTP_201_CREATED, tags=['shipments'])
def shipping_order():
    return "DEVELOPING...."  # TODO: 배송 주문 라우터 구현


@router.post("/cancel", status_code=status.HTTP_204_NO_CONTENT, tags=['shipments'])
def shipping_order():
    return "DEVELOPING...."  # TODO: 배송 취소 라우터 구현


@router.get("/track", status_code=status.HTTP_200_OK, tags=['shipments'])
def shipping_tracking():
    return "DEVELOPING...."  # TODO: 배송 조회 라우터 구현
