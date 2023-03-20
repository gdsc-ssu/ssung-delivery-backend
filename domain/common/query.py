from typing import Callable

from sqlalchemy.orm import Session
from fastapi import HTTPException


def transactional(query: Callable):
    def inner(session: Session, *args, **kwargs):
        try:
            result = query(session, *args, **kwargs)
            session.commit()
            return result

        except Exception as e:
            session.rollback()
            raise e

    return inner
