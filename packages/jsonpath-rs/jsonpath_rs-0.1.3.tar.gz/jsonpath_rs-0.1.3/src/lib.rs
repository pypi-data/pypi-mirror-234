use jsonpath_rust::JsonPathQuery;
use pyo3::prelude::*;
use serde_json::{Value, to_string};

#[pyfunction]
fn string_jsonpath_query(json_string: String, jsonpath: String) -> Option<String> {
    let json: Value = serde_json::from_str(&json_string).unwrap();
    let _jsonpath = json.path(&jsonpath).unwrap();
    let v = _jsonpath.clone();
    let result = to_string(&v).expect("to get string value");
    return Some(result);
}

#[pymodule]
fn jsonpath_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(string_jsonpath_query, m)?)?;
    Ok(())
}
