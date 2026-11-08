from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate


class EmailAlreadyExistsError(Exception):
    pass


def register_user(db: Session, user_data: UserCreate) -> User:

    repository = UserRepository(db)

    existing_user = repository.get_by_email(user_data.email)

    if existing_user:
        raise EmailAlreadyExistsError

    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password)
    )

    try:
        repository.create(user)

        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()
        raise EmailAlreadyExistsError from None