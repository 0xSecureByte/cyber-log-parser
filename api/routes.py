from fastapi import APIRouter, HTTPException
from models.log_models import LogModel
import log_parser  # Import the Rust parser module

log_routes = APIRouter()

@log_routes.post("/")
def parse_log_entry(log_entry: LogModel):
    try:
        # Call the Rust parser function
        parsed = log_parser.parse_log(log_entry.message)
        return {
            "timestamp": parsed[0],
            "log_level": parsed[1],
            "message": parsed[2]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))