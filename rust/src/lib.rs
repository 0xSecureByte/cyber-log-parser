use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn parse_log(log: &str) -> PyResult<(String, String, String)> {
    let parts: Vec<&str> = log.splitn(3, ' ').collect();
    if parts.len() < 3 {
        return Err(pyo3::exceptions::PyValueError::new_err("Invalid log format"));
    }
    let timestamp = parts[0].to_string();
    let log_level = parts[1].to_string();
    let message = parts[2].to_string();
    Ok((timestamp, log_level, message))
}

#[pymodule]
fn log_parser(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(parse_log, module)?)?;
    Ok(())
}