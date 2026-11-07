import time
from fastapi import FastAPI as FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
# import os, math, tempfile ,signal, subprocess,uuid
# from urllib.parse import urlparse, parse_qs



def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f" execution time: {end - start:.8f} seconds")
        return result
    return wrapper

app = FastAPI(title="Video API Backend 🚀")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

# app.include_router(n, prefix) 
@timer
@app.get("/")
def home(request: Request):
    request
    return {"message": "Backend Running Successfully on Server "}

# if __name__ == "__main__":
