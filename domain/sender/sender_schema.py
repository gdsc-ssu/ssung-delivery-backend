from pydantic import BaseModel


class SenderIn(BaseModel):
    sender_id: str
    sender_name: str
    password: str
    address: str
    sender_phone_number: str


class SenderOut(BaseModel):
    access_token: str
    token_type: str
    sender_name: str
