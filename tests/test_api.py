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

def test_parse_windows_log_entry():
    log_entry = "1\t2016-09-28\t04:30:30\tInfo\tCBS\tLoaded Servicing Stack v6.1.7601.23505 with Core: C:\\Windows\\winsxs\\amd64_microsoft-windows-servicingstack_31bf3856ad364e35_6.1.7601.23505_none_681aa442f6fed7f0\\cbscore.dll\tE23\tLoaded Servicing Stack <*> with Core: <*>\\cbscore.dll"
    response = client.post("/parse_windows_log/", json={"log_entry": log_entry})
    assert response.status_code == 200
    assert response.json() == {
        "line_id": "1",
        "date": "2016-09-28",
        "time": "04:30:30",
        "level": "Info",
        "component": "CBS",
        "content": "Loaded Servicing Stack v6.1.7601.23505 with Core: C:\\Windows\\winsxs\\amd64_microsoft-windows-servicingstack_31bf3856ad364e35_6.1.7601.23505_none_681aa442f6fed7f0\\cbscore.dll",
        "event_id": "E23",
        "event_template": "Loaded Servicing Stack <*> with Core: <*>\\cbscore.dll"
    }

def test_parse_linux_log_entry():
    log_entry = "1\tJun\t14\t15:16:01\tINFO\tsshd(pam_unix)\t19939\tauthentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4\tE16\tauthentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=<*>"
    response = client.post("/parse_linux_log/", json={"log_entry": log_entry})
    assert response.status_code == 200
    assert response.json() == {
        "line_id": "1",
        "month": "Jun",
        "date": "14",
        "time": "15:16:01",
        "level": "INFO",
        "component": "sshd(pam_unix)",
        "pid": "19939",
        "content": "authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4",
        "event_id": "E16",
        "event_template": "authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=<*>"
    }

def test_parse_macos_log_entry():
    log_entry = "1\tJul\t1\t09:00:55\tcalvisitor-10-105-160-95\tkernel\t0\t\tIOThunderboltSwitch<0>(0x0)::listenerCallback - Thunderbolt HPD packet for route = 0x0 port = 11 unplug = 0\tE252\tIOThunderboltSwitch<<*>>(<*>)::listenerCallback - Thunderbolt HPD packet for route = <*> port = <*> unplug = <*>"
    response = client.post("/parse_macos_log/", json={"log_entry": log_entry})
    assert response.status_code == 200
    assert response.json() == {
        "line_id": "1",
        "month": "Jul",
        "date": "1",
        "time": "09:00:55",
        "user": "calvisitor-10-105-160-95",
        "component": "kernel",
        "pid": "0",
        "address": "",
        "content": "IOThunderboltSwitch<0>(0x0)::listenerCallback - Thunderbolt HPD packet for route = 0x0 port = 11 unplug = 0",
        "event_id": "E252",
        "event_template": "IOThunderboltSwitch<<*>>(<*>)::listenerCallback - Thunderbolt HPD packet for route = <*> port = <*> unplug = <*>"
    }