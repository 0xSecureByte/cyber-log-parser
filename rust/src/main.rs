mod parser;

fn main() {
    println!("Starting Rust log parser...");
    let sample_log = "2024-09-20 12:34:56 INFO Sample log entry";
    let parsed_log = parser::parse_log(sample_log);
    println!("Parsed Log: {:?}", parsed_log);
}
