from fastapi import APIRouter

log_routes = APIRouter()

@log_routes.get("/")
def get_logs():
    return {"data": "Log parsing not implemented yet."}
