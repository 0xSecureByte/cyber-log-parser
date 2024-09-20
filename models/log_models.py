from pydantic import BaseModel

class LogModel(BaseModel):
    timestamp: str
    log_level: str
    message: str
