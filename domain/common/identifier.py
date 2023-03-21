import random
from sqlalchemy.orm import Session

from models import Word, Shipment
from utils import encode_id


def create_identifier(session: Session):
    words = [random.randint(1, session.query(Word).count()) for _ in range(3)]
    id_list = session.query(Word).filter(Word.id.in_(words)).all()
    id = encode_id([el.word for el in id_list])

    query = session.query(Shipment).filter_by(identifier=id).first()
    if query:
        create_identifier(session)

    return id
