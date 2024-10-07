# Cyber Log Parser

Cyber Log Parser is a GPU-accelerated log parsing tool designed to handle large volumes of cybersecurity logs with high performance and efficiency. Built using Python and Rust, this system leverages FastAPI for API management and Rust for high-performance log parsing. The project aims to efficiently ingest, process, and analyze log data, with potential extensions into machine learning.

## Features

* **GPU-Accelerated Parsing**: Optimized log parsing using Rust for performance-critical components.
* **FastAPI**: Python-based web API for log management and access.
* **Flexible Log Ingestion**: Handles various log formats for cybersecurity use cases.
* **Machine Learning Ready**: Placeholder for integrating ML models for anomaly detection, predictive analysis, etc.
* **Tech Stack**:
	+ **Rust**: High-performance log parsing logic.
	+ **Python**: FastAPI for API management and Python-based processing.
	+ **FastAPI**: RESTful API framework.
	+ **Pydantic**: Data validation and model creation.
	+ **Uvicorn**: ASGI server to run the FastAPI application.
* **File Structure**:
```plaintext
cyber-log-parser/
├── api/                      # FastAPI for handling API requests
│   ├── __init__.py
│   ├── main.py               # Entry point for the FastAPI app
│   └── routes.py             # API routes for log parsing and ML models
├── models/                   # Data models for logs, users, etc.
│   ├── __init__.py
│   └── log_model.py          # Log model structure (e.g., pydantic models)
├── processing/               # Python log parsing and ML modules
│   ├── __init__.py
│   ├── parser.py             # Python-based log parsing logic
│   └── ml_model.py           # Placeholder for ML model (if applicable)
├── rust/                     # Rust log parser implementation
│   ├── src/
│   │   ├── bin/
│   │   │   └── benchmark.rs  # Benchmarking tool for Rust log parser
│   │   ├── main.rs           # Entry point for Rust log parser
│   │   ├── parser.rs         # Rust log parsing logic
│   │   └── models.rs         # Data structures in Rust (for logs)
│   └── Cargo.toml            # Rust project dependencies
├── tests/                    # Unit tests for Python API and Rust logic
│   ├── test_api.py           # Test cases for the FastAPI endpoints
│   └── test_parser.rs        # Test cases for the Rust log parser
├── .gitignore                # Ignore unnecessary files (like __pycache__)
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
└── LICENSE                   # Open-source license file
```

## Installation and Setup

To set up the Cyber Log Parser project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/0xSecureByte/cyber-log-parser.git
   cd cyber-log-parser
   ```

2. **Install Python dependencies**:
   Ensure you have Python 3.7+ installed. Then, install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Build the Rust module using Maturin**:
   Then, build the Rust components and install them as a Python package:
   ```bash
   cd rust
   maturin develop
   cd ..
   ```

4. **Run the FastAPI server**:
   Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn api.main:app --reload
   ```

## Usage

#### API Endpoints

The Cyber Log Parser API is accessible at `http://127.0.0.1:8000/`. The following endpoints are available:

* **GET /**: Welcome message
* **POST /logs/**: Parse log entries using the Rust-based parser.

#### Parsing Logs via Rust

The Rust-based log parser processes logs based on timestamp, log level, and message.

#### Testing

To run the unit tests for the project, follow these steps:

##### Python (FastAPI) Tests

Run the Python unit tests for the API:
```bash
pytest tests/test_api.py
```

##### Rust Tests

Run the Rust unit tests for the log parser:
```bash
cargo test
```
Future Roadmap
================

The following features are planned for future development:

### Performance Enhancements

* Integrate GPU-accelerated parsing using CUDA/GPUs to improve processing speed.

### Logging and Error Handling

* Develop comprehensive logging and error-handling mechanisms to ensure system reliability and fault tolerance.

### Advanced Log Analysis

* Implement machine learning models for advanced log analysis, enabling more sophisticated insights and pattern detection.

### Log Format Support

* Add support for multiple log formats, including JSON and CSV, to increase the versatility of the log parser.

### API Expansion

* Expand API functionality to include features such as search and filter logs, enhancing the user experience and utility of the API.


## Benchmarking

The Cyber Log Parser includes a Rust-based benchmarking tool to evaluate the performance of the log parsing API. This tool can simulate a large number of concurrent HTTP requests to the API, providing insights into its performance under load.

### Running the Benchmark

To run the benchmark, follow these steps:

1. **Navigate to the Rust directory**:
   ```bash
   cd rust/
   ```

2. **Execute the benchmark**:
   Run the benchmark with the desired number of requests and batch size:
   ```bash
   cargo run --bin benchmark <number_of_requests> <batch_size>
   ```

   Replace `<number_of_requests>` with the total number of requests you want to simulate, and `<batch_size>` with the number of concurrent requests to send in each batch.

### Benchmark Output

The benchmark tool provides the following output:

- **Total Time Taken**: The total duration for processing all requests.
- **Successful Requests**: The number of requests that were successfully processed.
- **Failed Requests**: The number of requests that failed due to client or server errors. (Depends on the server's load)
- **Average Time Per Request**: The average time taken to process each request.
- **Progress Bar**: A visual CLI based representation of the progress of the benchmark.

This tool is useful for stress testing the API and identifying potential bottlenecks or performance issues.

Contributions
------------

Contributions to the project are highly valued and encouraged. To contribute, please follow these steps:

1. **Fork the repository**: Create a copy of the project repository under your GitHub account.
2. **Create a new branch**: From your forked repository, create a new branch with a descriptive name (e.g., `feature/new-log-format-support`).
3. **Make your changes**: Implement your desired feature or fix, adhering to the project's coding standards and best practices.
4. **Open a pull request**: Submit your changes to the original project repository, providing a detailed description of your work and the benefits it brings.

By contributing to this project, you will help shape its future and make it more useful for the community.