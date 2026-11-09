from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.refresh_token import (
    generate_refresh_token,
    hash_refresh_token
)
from app.modules.users.session_models import UserSession
from app.modules.users.session_repository import SessionRepository


def create_user_session(db: Session, user_id: int) -> str:
    refresh_token = generate_refresh_token()

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    user_session = UserSession(
        user_id=user_id,
        refresh_token_hash=hash_refresh_token(refresh_token),
        expires_at=expires_at
    )

    repository = SessionRepository(db)

    try:
        repository.create(user_session)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return refresh_token


def rotate_refresh_token(db: Session, refresh_token: str) -> tuple[int, str]:
    repository = SessionRepository(db)

    user_session = repository.get_by_token_hash(hash_refresh_token(refresh_token))

    if user_session is None:
        raise ValueError("Invalid or expired refresh token")

    new_refresh_token = generate_refresh_token()

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    repository.update_token(
        user_session,
        hash_refresh_token(new_refresh_token),
        expires_at
    )

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return user_session.user_id, new_refresh_token