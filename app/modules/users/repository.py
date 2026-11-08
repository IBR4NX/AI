from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.modules.users.models import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:

        statement = select(User).where(User.email == email)

        return self.db.scalar(statement)
    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)
    
    def create(self, user: User) -> User:

        self.db.add(user)
        self.db.flush()
        return user
    def update_name(self, user: User) -> User:
        stmt =(
        update(User).where(User.id == user.id).values(name=user.name).execution_options(synchronize_session="fetch")
        )

        return stmt