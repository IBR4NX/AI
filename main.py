from fastapi import FastAPI as FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
# import os, math, tempfile ,signal, subprocess,uuid
# from urllib.parse import urlparse, parse_qs

#
app = FastAPI(title="Video API Backend 🚀")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

# app.include_router(n, prefix) 
@app.get("/")
def home(request: Request):
    request
    return {"message": "Backend Running Successfully 🎯"}

# if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
