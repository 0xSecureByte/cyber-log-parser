use rand::seq::SliceRandom;
use reqwest::Client;
use rand::Rng;
use chrono::{Utc, Duration};
use std::env;
use futures;
use tokio::task;
use tokio::time::Instant;
use indicatif::ProgressBar;
use indicatif::ProgressStyle;

async fn send_request(client: &Client, url: &str, data: serde_json::Value) -> Result<reqwest::StatusCode, reqwest::Error> {
    let response = client.post(url)
        .json(&data)
        .send()
        .await?;
    Ok(response.status())
}

async fn batch_requests(client: &Client, url: &str, batch_size: usize) -> Vec<reqwest::StatusCode> {
    let mut tasks = Vec::new();
    for _ in 0..batch_size {
        let random_timestamp = Utc::now() + Duration::seconds(rand::thread_rng().gen_range(-3600..3600));
        let random_log_level = ["DEBUG", "INFO", "WARNING", "ERROR"].choose(&mut rand::thread_rng()).unwrap();
        let random_message: String = rand::thread_rng()
            .sample_iter(&rand::distributions::Alphanumeric)
            .take(100)
            .map(char::from)
            .collect();

        let data = serde_json::json!({
            "timestamp": random_timestamp.to_rfc3339(),
            "log_level": random_log_level,
            "message": random_message
        });

        let client_clone = client.clone();
        let url_clone = url.to_string();
        tasks.push(task::spawn(async move {
            send_request(&client_clone, &url_clone, data).await.unwrap_or(reqwest::StatusCode::INTERNAL_SERVER_ERROR)
        }));
    }

    let results = futures::future::join_all(tasks).await;
    results.into_iter().map(|res| res.unwrap()).collect()
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: cargo run --bin benchmark <number_of_requests> <batch_size>");
        return;
    }

    let num_requests: usize = args[1].parse().expect("Invalid number of requests");
    let batch_size: usize = args[2].parse().expect("Invalid batch size");

    let client = Client::new();
    let url = "http://127.0.0.1:8000/logs/";

    let start_time = Instant::now();
    let mut results = Vec::new();

    // Initialize the progress bar
    let pb = ProgressBar::new(num_requests as u64);
    println!("\n\nStarting benchmark...\n");
    pb.set_style(ProgressStyle::default_bar()
        .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} ({eta})")
        .expect("REASON"));

    for i in (0..num_requests).step_by(batch_size) {
        let current_batch_size = std::cmp::min(batch_size, num_requests - i);
        let batch_results = batch_requests(&client, url, current_batch_size).await;
        results.extend(batch_results);

        // Update the progress bar
        pb.inc(current_batch_size as u64);
    }

    pb.finish_with_message("Requests completed");

    let total_time = start_time.elapsed();
    let failed_requests: Vec<_> = results.iter().filter(|&&status| status.is_client_error() || status.is_server_error()).collect();

    println!("\n\nTotal time taken for processing {} requests: {:.2?} seconds", num_requests, total_time);
    println!("Final Results: {} requests were successfully processed.", results.len() - failed_requests.len());
    println!("Failed Requests: {} requests failed.", failed_requests.len());
    println!("Average time taken per request: {:.7?} seconds", total_time.as_secs_f64() / num_requests as f64);
    println!("Total time elapsed: {:.2?}", total_time);
}