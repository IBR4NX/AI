from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
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

        return {**user.__dict__}

    except IntegrityError:
        db.rollback()
        raise EmailAlreadyExistsError from None

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    repository = UserRepository(db)

    user = repository.get_by_email(email)

    if user is None:
        return None

    if not verify_password(password, user.password):
        return None

    return user