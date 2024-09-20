pub fn parse_log(log: &str) -> (&str, &str, &str) {
    let timestamp = &log[0..19];
    let log_level = &log[20..25].trim();
    let message = &log[26..];
    (timestamp, log_level, message)
}
