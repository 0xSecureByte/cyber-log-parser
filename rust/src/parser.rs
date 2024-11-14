pub fn parse_log(log: &str) -> Option<(&str, &str, &str)> {
    let parts: Vec<&str> = log.splitn(3, ' ').collect();
    if parts.len() < 3 {
        return None; // Return None if the log format is incorrect
    }
    let timestamp = parts[0];
    let log_level = parts[1];
    let message = parts[2];
    Some((timestamp, log_level, message))
}

pub fn parse_windows_log(log: &str) -> Option<(String, String, String, String, String, String, String, String)> {
    let parts: Vec<&str> = log.split('\t').collect();
    if parts.len() < 8 {
        return None; // Return None if the log format is incorrect
    }
    let line_id = parts[0].to_string();
    let date = parts[1].to_string();
    let time = parts[2].to_string();
    let level = parts[3].to_string();
    let component = parts[4].to_string();
    let content = parts[5].to_string();
    let event_id = parts[6].to_string();
    let event_template = parts[7].to_string();
    
    Some((line_id, date, time, level, component, content, event_id, event_template))
}

pub fn parse_linux_log(log: &str) -> Option<(String, String, String, String, String, String, String, String, String, String)> {
    let parts: Vec<&str> = log.split('\t').collect();
    if parts.len() < 9 {
        return None; // Return None if the log format is incorrect
    }
    let line_id = parts[0].to_string();
    let month = parts[1].to_string();
    let date = parts[2].to_string();
    let time = parts[3].to_string();
    let level = parts[4].to_string();
    let component = parts[5].to_string();
    let pid = parts[6].to_string();
    let content = parts[7].to_string();
    let event_id = parts[8].to_string();
    let event_template = parts[9].to_string();

    Some((line_id, month, date, time, level, component, pid, content, event_id, event_template))
}