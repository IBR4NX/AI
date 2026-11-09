from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.users.session_models import UserSession


class SessionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_session: UserSession) -> UserSession:
        self.db.add(user_session)
        self.db.flush()
        return user_session

    def get_by_token_hash(self, token_hash: str) -> UserSession | None:
        statement = select(UserSession).where(
            UserSession.refresh_token_hash == token_hash,
            UserSession.revoked_at.is_(None),
            UserSession.expires_at > datetime.now(timezone.utc)
        )

        return self.db.scalar(statement)

    def update_token(
        self,
        user_session: UserSession,
        new_token_hash: str,
        expires_at: datetime
    ) -> None:
        user_session.refresh_token_hash = new_token_hash
        user_session.expires_at = expires_at

    def revoke(self, user_session: UserSession) -> None:
        user_session.revoked_at = datetime.now(timezone.utc)
    
    def get_by_user_id(self, user_id: int) -> UserSession | None:
        statement = select(UserSession).where(
            UserSession.user_id == user_id,
            # UserSession.revoked_at.is_(None),
            # UserSession.expires_at > datetime.now(timezone.utc)
        )

        return self.db.scalar(statement)