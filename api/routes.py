from fastapi import APIRouter, HTTPException, File, UploadFile
from models.log_models import LogModel
import log_parser  # Import the Rust parser module
import csv

log_routes = APIRouter()

@log_routes.post("/")
def parse_log_entry(log_entry: LogModel):
    try:
        # Convert the LogModel to a JSON string
        log_json = log_entry.json()
        # Call the Rust parser function
        parsed = log_parser.parse_log(log_json)
        return {
            "timestamp": parsed[0],
            "log_level": parsed[1],
            "message": parsed[2]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@log_routes.post("/parse_windows_log/")
async def parse_windows_log_entry(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()
    decoded_contents = contents.decode("utf-8").splitlines()
    csv_reader = csv.reader(decoded_contents, delimiter=',')
    
    parsed_logs = []
    
    # Skip the header
    next(csv_reader)

    for row in csv_reader:
        if len(row) < 8:
            continue  # Skip rows that do not have enough columns
        log_entry = "\t".join(row)  # Join the row back into a tab-separated string
        parsed = log_parser.parse_windows_log(log_entry)
        if parsed is not None:
            parsed_logs.append({
                "line_id": parsed[0],
                "date": parsed[1],
                "time": parsed[2],
                "level": parsed[3],
                "component": parsed[4],
                "content": parsed[5],
                "event_id": parsed[6],
                "event_template": parsed[7],
            })

    return {"parsed_windows_logs": parsed_logs}

@log_routes.post("/parse_linux_log/")
async def parse_linux_log_entry(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()
    decoded_contents = contents.decode("utf-8").splitlines()
    csv_reader = csv.reader(decoded_contents, delimiter=',')
    
    parsed_logs = []
    
    # Skip the header
    next(csv_reader)

    for row in csv_reader:
        if len(row) < 10:
            continue  # Skip rows that do not have enough columns
        log_entry = "\t".join(row)  # Join the row back into a tab-separated string
        parsed = log_parser.parse_linux_log(log_entry)
        if parsed is not None:
            parsed_logs.append({
                "line_id": parsed[0],
                "month": parsed[1],
                "date": parsed[2],
                "time": parsed[3],
                "level": parsed[4],
                "component": parsed[5],
                "pid": parsed[6],
                "content": parsed[7],
                "event_id": parsed[8],
                "event_template": parsed[9],
            })

    return {"parsed_linux_logs": parsed_logs}


@log_routes.post("/parse_mac_log/")
async def parse_mac_log_entry(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()
    decoded_contents = contents.decode("utf-8").splitlines()
    csv_reader = csv.reader(decoded_contents, delimiter=',')
    
    parsed_logs = []
    
    # Skip the header
    next(csv_reader)

    for row in csv_reader:
        if len(row) < 10:
            continue  # Skip rows that do not have enough columns
        log_entry = "\t".join(row)  # Join the row back into a tab-separated string
        parsed = log_parser.parse_mac_log(log_entry)
        if parsed is not None:
            parsed_logs.append({
                "line_id": parsed[0],
                "month": parsed[1],
                "date": parsed[2],
                "time": parsed[3],
                "user": parsed[4],
                "component": parsed[5],
                "pid": parsed[6],
                "address": parsed[7],
                "content": parsed[8],
            })

    return {"parsed_mac_logs": parsed_logs}