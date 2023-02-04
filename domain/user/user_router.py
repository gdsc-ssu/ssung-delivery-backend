from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from database import create_session
from domain.user import user_schema
from utils import verify_password, create_access_token
from domain.user import user_crud

router = APIRouter(prefix="/api/user") #url 라우팅

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def user_create(user_in:user_schema.UserIn, session=Depends(create_session)):
    """
    유저를 생성합니다.

    Args:
        user_in (user_schema.UserIn): 유저 생성을 위한 입력 형태 (유저 이름, 비밀번호, 주소, 핸드폰 번호)
        session (Session, optional): DB 커넥션을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 409에러 이미 유저가 존재
    """
    try:
        user = user_crud.get_user(session, user_in.user_name)
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already Exists.")
        
        user_crud.create_user(session=session, user_in=user_in)
        
    
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_csode=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/login", response_model=user_schema.UserOut, tags=["users"])
def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(), session=Depends(create_session)):
    """
    로그인 토큰을 검증해 로그인을 진행합니다.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): fastapi제공 토큰 제공 폼 타입. Defaults to Depends().
        session (Session, optional): DB연결을 위한 세션. Defaults to Depends(create_session).

    Raises:
        HTTPException: 401 로그인 에러
        HTTPException: 500 서버 에러

    Returns:
        Userout: User 출력 모델
    """
    try:
        user = user_crud.get_user(session, form_data.username)
        if user and verify_password(form_data.password, user.password):
            access_token = create_access_token(subject=user.user_name)
            return {"access_token": access_token,
                    "token_type":"bearer",
                    "username":user.user_name
                    }
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


