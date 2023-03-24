from typing import Callable, TypeVar, ParamSpec, Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException

T = TypeVar("T")
P = ParamSpec("P")


def transactional(query: Callable[P, T]):
    def inner(session: Session, *args: P.args, **kwargs: P.kwargs) -> Optional[T]:
        try:
            result = query(session, *args, **kwargs)
            session.commit()
            return result

        except Exception as e:
            session.rollback()
            raise e

    return inner
