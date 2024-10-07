use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use serde::Deserialize;

#[derive(Deserialize)]
struct LogEntry {
    timestamp: String,
    log_level: String,
    message: String,
}

#[pyfunction]
fn parse_log(log: &str) -> PyResult<(String, String, String)> {
    let log_entry: LogEntry = serde_json::from_str(log)
        .map_err(|_| pyo3::exceptions::PyValueError::new_err("Invalid log format"))?;
    
    Ok((log_entry.timestamp, log_entry.log_level, log_entry.message))
}

#[pymodule]
fn log_parser(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(parse_log, module)?)?;
    Ok(())
}