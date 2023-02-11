from pydantic import BaseModel
from typing import Optional


class ShipmentIn(BaseModel):
    content_name: str
    receiver_name: Optional[str]
    receiver_phone_number: Optional[str]
    destination: str
    shipment_detail: Optional[str]
