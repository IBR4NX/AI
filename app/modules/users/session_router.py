from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.access_token import create_access_token
from app.core.dependencies import export_user_id
from app.database.session import get_db
from app.modules.users.schemas import UserCreate

from app.modules.users.session_repository import SessionRepository
from app.modules.users.session_schemas import TokenResponse,TokenRefresh, UserLoginResponse, UserSessionResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.modules.users.session_service import create_user_session, rotate_refresh_token
from app.modules.users.service import (
    register_user,
    EmailAlreadyExistsError,
    authenticate_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=UserLoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        form_data.username.strip().lower(),
        form_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )        
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_user_session(db,user.id)
    user_response = UserLoginResponse(
            name=user.name,
            email=user.email,
            access_token=access_token,
            refresh_token=refresh_token
        )
    return user_response

@router.post("/register", response_model=UserLoginResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    try:
        user= register_user(db, user_data)
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_user_session(db, user.id)
        user_response = UserLoginResponse(
            name=user.name,
            email=user.email,
            access_token=access_token,
            refresh_token=refresh_token
        )
        return user_response

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
    refresh_token:TokenRefresh ,
    db: Session = Depends(get_db)
):
    exp=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    if not refresh_token:
        exp.detail="Refresh token not found"
        raise exp
    try:
        user_id, new_refresh_token = rotate_refresh_token(db, refresh_token.refresh_token)
        access_token = create_access_token({"sub": str(user_id)})
        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)

    except ValueError:
        exp.detail="Invalid or expired refresh token"
        raise exp

@router.get("/session", status_code=status.HTTP_200_OK)
def check_session(
    user_id: int = Depends(export_user_id),
    db: Session = Depends(get_db)
):
    repository = SessionRepository(db)
    session = repository.get_by_user_id(user_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session