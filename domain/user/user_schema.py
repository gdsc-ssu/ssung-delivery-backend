from pydantic import BaseModel
class UserIn(BaseModel):
    user_name:str
    password:str
    address:str
    is_user:bool


class UserOut(BaseModel):
    access_token:str
    token_type:str
    username:str