from pydantic import BaseModel

from app.modules.users.schemas import UserResponse


class UserLoginResponse(UserResponse):
    access_token: str
    refresh_token: str  

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
class TokenRefresh(BaseModel):
    username: str
    refresh_token: str

class UserSessionResponse(BaseModel):
    user_id: int
    refresh_token_hash: str
    expires_at: str
    revoked_at: str | None = None
    