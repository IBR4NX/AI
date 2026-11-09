from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.modules.users.session_router import router as users_router
from app.core.healthy import router as healthy_router
app = FastAPI(
    title="AI API by Ibrahim Al-Mekhlafi",
    version="1.0.0"
)

app.include_router(healthy_router)
app.include_router(users_router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")
    
