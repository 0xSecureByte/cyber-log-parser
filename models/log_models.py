from pydantic import BaseModel
from datetime import datetime

class LogModel(BaseModel):
    timestamp: datetime  # Expecting a datetime object
    log_level: str       # e.g., "INFO", "ERROR", etc.
    message: str         # The log message content
