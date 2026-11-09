from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import  export_user_id
from app.modules.users.repository import UserRepository

router = APIRouter(
    prefix="/users",
    tags=[" Users"]
)
@router.get("/my-profile")
def get_profile(
    user_id: int = Depends(export_user_id),
        db: Session = Depends(get_db)
):
    repository = UserRepository(db)
    user = repository.get_by_id(int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return 
