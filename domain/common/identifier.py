import random
from sqlalchemy.orm import Session

from models import Word, Shipment
from utils import encode_id


def create_identifier(session: Session) -> str:
    words = [random.randint(1, session.query(Word).count()) for _ in range(3)]
    id_list = session.query(Word).filter(Word.id.in_(words)).all()
    return encode_id([el.word for el in id_list])
