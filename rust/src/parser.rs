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