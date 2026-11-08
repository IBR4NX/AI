from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.database.session import get_db
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserResponse,TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.core.dependencies import get_current_user, export_user_id
from app.modules.users.service import (
    register_user,
    EmailAlreadyExistsError,
    authenticate_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
@router.post("/login", response_model=TokenResponse)
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

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return TokenResponse(access_token=access_token)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    try:
        return register_user(db, user_data)

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

@router.get("/me")
def get_profile(
    user: User = Depends(get_current_user)
):
    return user

@router.get("/test")
def get_tasks(
    user_id: int = Depends(export_user_id)
):
    return {
        "user_id": user_id,
        "message": "Tasks retrieved successfully"
    }