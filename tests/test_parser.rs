#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_log() {
        let log = "2024-09-20 12:34:56 INFO Sample log entry";
        let (timestamp, log_level, message) = parse_log(log);
        assert_eq!(timestamp, "2024-09-20 12:34:56");
        assert_eq!(log_level, "INFO");
        assert_eq!(message, "Sample log entry");
    }
}
