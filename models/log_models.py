from pydantic import BaseModel

class LogModel(BaseModel):
    timestamp: str       # formatted timestamp e.g., "2024-02-20T12:00:00Z"
    log_level: str       # e.g., "INFO", "ERROR", etc.
    message: str         # The log message content

