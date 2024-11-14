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

#[pyfunction]
fn parse_windows_log(log: &str) -> PyResult<(String, String, String, String, String, String, String, String)> {
    let parts: Vec<&str> = log.split('\t').collect();
    if parts.len() < 8 {
        return Err(pyo3::exceptions::PyValueError::new_err("Invalid log format"));
    }
    let line_id = parts[0].to_string();
    let date = parts[1].to_string();
    let time = parts[2].to_string();
    let level = parts[3].to_string();
    let component = parts[4].to_string();
    let content = parts[5].to_string();
    let event_id = parts[6].to_string();
    let event_template = parts[7].to_string();
    
    Ok((line_id, date, time, level, component, content, event_id, event_template))
}

#[pyfunction]
fn parse_linux_log(log: &str) -> PyResult<(String, String, String, String, String, String, String, String, String, String)> {
    let parts: Vec<&str> = log.split('\t').collect();
    if parts.len() < 9 {
        return Err(pyo3::exceptions::PyValueError::new_err("Invalid log format"));
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
    let event_template = if parts.len() > 9 { parts[9].to_string() } else { "".to_string() };

    Ok((line_id, month, date, time, level, component, pid, content, event_id, event_template))
}

#[pyfunction]
fn parse_mac_log(log: &str) -> PyResult<(String, String, String, String, String, String, String, String, String)> {
    let parts: Vec<&str> = log.split('\t').collect();
    if parts.len() < 8 {
        return Err(pyo3::exceptions::PyValueError::new_err("Invalid log format"));
    }
    let line_id = parts[0].to_string();
    let month = parts[1].to_string();
    let date = parts[2].to_string();
    let time = parts[3].to_string();
    let user = parts[4].to_string();
    let component = parts[5].to_string();
    let pid = parts[6].to_string();
    let address = parts[7].to_string();
    let content = parts[8].to_string();
    
    Ok((line_id, month, date, time, user, component, pid, address, content))
}

#[pymodule]
fn log_parser(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(parse_log, module)?)?;
    module.add_function(wrap_pyfunction!(parse_windows_log, module)?)?;
    module.add_function(wrap_pyfunction!(parse_linux_log, module)?)?;
    module.add_function(wrap_pyfunction!(parse_mac_log, module)?)?;
    Ok(())
}