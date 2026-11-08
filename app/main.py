from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db

app = FastAPI(
    title="My API",
    version="1.0.0"
)
from app.modules.users.router import router as users_router

app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/db-check")
def database_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "message": "Database connected successfully"
    }