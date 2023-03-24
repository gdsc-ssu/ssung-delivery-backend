import sys
import traceback
from typing import Callable, TypeVar, ParamSpec

from fastapi import HTTPException
from starlette import status

T = TypeVar("T")
P = ParamSpec("P")


def exception_handler(service: Callable[P, T]):
    def inner(*args: P.args, **kwargs: P.kwargs) -> T | dict:
        try:
            return service(*args, **kwargs) or {"ok": True}

        except HTTPException as e:
            raise e

        except Exception:
            traceback.print_exception(*sys.exc_info())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inner
