import enum
from typing import Optional

from pydantic import BaseModel


class ShipmentIn(BaseModel):
    content_name: str
    receiver_name: Optional[str]
    receiver_phone_number: Optional[str]
    destination: str
    shipment_detail: Optional[str]
    identifier: list


class ShipmentOut(BaseModel):
    receiver_name: Optional[str]
    receiver_phone_number: Optional[str]
    destination: str
    shipment_detail: Optional[str] = None
    identifier: Optional[list] = None
    history: Optional[list] = None
    status: Optional[enum.Enum] = None
