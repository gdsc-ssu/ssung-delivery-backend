from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from database import create_session
from domain.user import user_schema
from utils import verify_password, create_access_token
from domain.user import user_crud

router = APIRouter(prefix="/api/user")

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(user_in:user_schema.UserIn, session=Depends(create_session)):
    user = user_crud.get_exisiting_user(session, user_in.user_name)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already Exists.")
    
    user_crud.create_user(session=session, user_in=user_in)


@router.post("/login", response_model=user_schema.UserOut)
def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(), session=Depends(create_session)):
    user = user_crud.get_user(session, form_data.username)
    if user and verify_password( form_data.password, user.password):
        access_token = create_access_token(subject=user.user_name)
        return {"access_token": access_token,
                "token_type":"bearer",
                "username":user.user_name
                }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


