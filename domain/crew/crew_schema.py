from pydantic import BaseModel


class CrewIn(BaseModel):
    crew_name: str
    crew_id: str
    password: str
    area: str
    crew_phone_number: str


class CrewOut(BaseModel):
    access_token: str
    token_type: str
    crew_name: str
