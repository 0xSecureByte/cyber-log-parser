from fastapi import FastAPI
from .routes import log_routes

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Cyber Log Parser"}

app.include_router(log_routes, prefix="/logs")
