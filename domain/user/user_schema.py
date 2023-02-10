from pydantic import BaseModel


class UserIn(BaseModel):
    user_name: str
    password: str
    address: str
    phone_number: str


class UserOut(BaseModel):
    access_token: str
    token_type: str
    username: str
