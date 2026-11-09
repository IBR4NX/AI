from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.access_token import decode_access_token
from app.database.session import get_db
from app.modules.users.models import User
from app.modules.users.repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def export_user_id(
    token: str = Depends(oauth2_scheme)
) -> int:

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if not isinstance(user_id, str) or not user_id.isdigit():
            raise ValueError("Invalid user ID")

        return int(user_id)

    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if not isinstance(user_id, str) or not user_id.isdigit():
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    repository = UserRepository(db)
    user = repository.get_by_id(int(user_id))

    if user is None:
        raise credentials_exception

    return user