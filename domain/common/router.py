import sys
import traceback
from typing import Callable

from fastapi import HTTPException
from starlette import status


def exception_handler(service: Callable):
    def inner(*args, **kwargs):
        try:
            return service(*args, **kwargs) or {"ok": True}

        except HTTPException as e:
            raise e

        except Exception:
            traceback.print_exception(*sys.exc_info())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return inner
