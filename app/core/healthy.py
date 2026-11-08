from sqlalchemy import text
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

router = APIRouter(
    prefix="/healthy",
    tags=["Healthy"]
)

@router.get("/db-check")
def database_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "Database connected successfully"}
    except Exception as e:
        return {"message": "Database connection failed", "error": str(e)}
    

