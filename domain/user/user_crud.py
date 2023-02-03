from utils import get_hash_password
from sqlalchemy.orm import Session
from models import User
from domain.user import user_schema

def create_user(session:Session, user_in:user_schema.UserIn):
    user = User(user_name=user_in.user_name, password=get_hash_password(user_in.password),
                    address=user_in.address, is_user=user_in.is_user)

    session.add(user)


def get_exisiting_user(session:Session, user_name:str):
    print(user_name)
    query = session.query(User).filter(User.user_name==user_name).first()
    return query


def get_user(session:Session, user_name:str):
    with session:
        return session.query(User).filter(User.user_name==user_name).first()
    

