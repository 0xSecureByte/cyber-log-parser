def parse_log(log_line: str) -> dict:
    # Placeholder parsing logic
    parsed_log = {
        "timestamp": log_line[:19],
        "log_level": log_line[20:25].strip(),
        "message": log_line[26:]
    }
    return parsed_log
