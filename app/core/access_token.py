from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings
from app.core.security import hash_password
    

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    payload = data.copy()

    payload.update({
        "exp": datetime.now(timezone.utc)
        + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)),
        "type": "access"
    })

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

    if payload.get("type") != "access":
        raise jwt.InvalidTokenError("Invalid token type")

    return payload
