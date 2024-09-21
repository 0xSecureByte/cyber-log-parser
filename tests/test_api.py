from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Cyber Log Parser"}

def test_parse_log_entry():
    log_entry = {"message": "2024-09-20 12:34:56 INFO Sample log entry"}
    response = client.post("/logs/", json=log_entry)
    assert response.status_code == 200
    assert response.json() == {
        "timestamp": "2024-09-20 12:34:56",
        "log_level": "INFO",
        "message": "Sample log entry"
    }

def test_invalid_log_entry():
    log_entry = {"message": "Invalid log format"}
    response = client.post("/logs/", json=log_entry)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid log format"}