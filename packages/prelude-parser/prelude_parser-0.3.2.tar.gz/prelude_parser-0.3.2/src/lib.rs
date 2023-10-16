use std::collections::HashMap;
use std::fs::read_to_string;
use std::path::PathBuf;

use chrono::{Datelike, NaiveDate};
use pyo3::create_exception;
use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use pyo3::types::{IntoPyDict, PyDict, PyList};
use roxmltree::Document;

create_exception!(_prelude_parser, FileNotFoundError, PyException);
create_exception!(_prelude_parser, InvalidFileTypeError, PyException);
create_exception!(_prelude_parser, ParsingError, PyException);

fn to_snake(camel_string: &str) -> String {
    let mut snake_string = String::with_capacity(
        camel_string.len() + camel_string.chars().filter(|c| c.is_uppercase()).count(),
    );

    let mut chars = camel_string.chars().peekable();
    while let Some(c) = chars.next() {
        snake_string.push(c);
        if let Some(next) = chars.peek() {
            if next.is_uppercase() && c != '_' {
                snake_string.push('_');
            }
        }
    }

    snake_string.to_lowercase()
}

fn py_list_append<'py>(
    py: Python<'py>,
    value: Option<&str>,
    list: &'py PyList,
) -> PyResult<&'py PyList> {
    let datetime = py.import("datetime")?;
    let date = datetime.getattr("date")?;

    match value {
        Some(t) => match t.parse::<usize>() {
            Ok(int_val) => list.append(int_val)?,
            Err(_) => match t.parse::<f64>() {
                Ok(float_val) => list.append(float_val)?,
                Err(_) => match NaiveDate::parse_from_str(t, "%d-%b-%Y") {
                    Ok(dt) => {
                        let py_date = date.call1((dt.year(), dt.month(), dt.day()))?;
                        list.append(py_date)?;
                    }
                    Err(_) => list.append(t)?,
                },
            },
        },
        None => list.append(py.None())?,
    };

    Ok(list)
}

fn add_item<'py>(
    py: Python<'py>,
    key: &str,
    value: Option<&str>,
    form_data: &'py PyDict,
) -> PyResult<&'py PyDict> {
    let datetime = py.import("datetime")?;
    let date = datetime.getattr("date")?;

    match value {
        Some(t) => match t.parse::<usize>() {
            Ok(int_val) => form_data.set_item(key, int_val)?,
            Err(_) => match t.parse::<f64>() {
                Ok(float_val) => form_data.set_item(key, float_val)?,
                Err(_) => match NaiveDate::parse_from_str(t, "%d-%b-%Y") {
                    Ok(dt) => {
                        let py_date = date.call1((dt.year(), dt.month(), dt.day()))?;
                        form_data.set_item(key, py_date)?;
                    }
                    Err(_) => form_data.set_item(key, t)?,
                },
            },
        },
        None => form_data.set_item(key, py.None())?,
    };

    Ok(form_data)
}

fn parse_xml<'py>(py: Python<'py>, xml_file: &PathBuf, short_names: bool) -> PyResult<&'py PyDict> {
    let reader = read_to_string(xml_file);

    match reader {
        Ok(r) => match Document::parse(&r) {
            Ok(doc) => {
                let mut data: HashMap<String, Vec<&PyDict>> = HashMap::new();
                let tree = doc.root_element();
                for form in tree.children() {
                    let form_name = if short_names {
                        form.tag_name().name().to_owned().to_lowercase()
                    } else {
                        to_snake(form.tag_name().name())
                    };
                    if !form_name.is_empty() {
                        if let Some(d) = data.get_mut(&form_name) {
                            let form_data = PyDict::new(py);
                            for child in form.children() {
                                if child.is_element() && child.tag_name().name() != "" {
                                    let key = if short_names {
                                        child.tag_name().name().to_owned().to_lowercase()
                                    } else {
                                        to_snake(child.tag_name().name())
                                    };
                                    add_item(py, &key, child.text(), form_data)?;
                                };
                            }
                            d.push(form_data);
                        } else {
                            let mut items: Vec<&PyDict> = Vec::new();
                            let form_data = PyDict::new(py);
                            for child in form.children() {
                                if child.is_element() && child.tag_name().name() != "" {
                                    let key = if short_names {
                                        child.tag_name().name().to_owned().to_lowercase()
                                    } else {
                                        to_snake(child.tag_name().name())
                                    };
                                    add_item(py, &key, child.text(), form_data)?;
                                }
                            }
                            items.push(form_data.into_py_dict(py));
                            data.insert(form_name, items);
                        }
                    }
                }
                return Ok(data.into_py_dict(py));
            }
            Err(e) => Err(ParsingError::new_err(format!(
                "Error parsing xml file: {:?}",
                e
            ))),
        },
        Err(e) => Err(ParsingError::new_err(format!(
            "Error parsing xml file: {:?}",
            e
        ))),
    }
}

fn parse_xml_pandas<'py>(
    py: Python<'py>,
    xml_file: &PathBuf,
    short_names: bool,
) -> PyResult<&'py PyDict> {
    let reader = read_to_string(xml_file);

    match reader {
        Ok(r) => match Document::parse(&r) {
            Ok(doc) => {
                let data = PyDict::new(py);
                let tree = doc.root_element();

                for form in tree.children() {
                    for child in form.children() {
                        if child.is_element() && child.tag_name().name() != "" {
                            let column = if short_names {
                                child.tag_name().name().to_owned().to_lowercase()
                            } else {
                                to_snake(child.tag_name().name())
                            };
                            if let Some(c) = data.get_item(column.clone()) {
                                py_list_append(py, child.text(), c.extract()?)?;
                                data.set_item(column, c)?;
                            } else {
                                let list = PyList::empty(py);
                                py_list_append(py, child.text(), list)?;
                                data.set_item(column, list)?;
                            }
                        }
                    }
                }
                return Ok(data.into_py_dict(py));
            }
            Err(e) => Err(ParsingError::new_err(format!(
                "Error parsing xml file: {:?}",
                e
            ))),
        },
        Err(e) => Err(ParsingError::new_err(format!(
            "Error parsing xml file: {:?}",
            e
        ))),
    }
}

fn validate_file(xml_file: &PathBuf) -> PyResult<()> {
    if !xml_file.is_file() {
        return Err(FileNotFoundError::new_err(format!(
            "File not found: {:?}",
            xml_file
        )));
    } else if xml_file.extension().unwrap() != "xml" {
        return Err(InvalidFileTypeError::new_err(format!(
            "{:?} is not an xml file",
            xml_file
        )));
    }

    Ok(())
}

#[pyfunction]
fn _parse_flat_file_to_dict(py: Python, xml_file: PathBuf, short_names: bool) -> PyResult<&PyDict> {
    validate_file(&xml_file)?;
    let data = parse_xml(py, &xml_file, short_names)?;

    Ok(data)
}

#[pyfunction]
fn _parse_flat_file_to_pandas_dict(
    py: Python,
    xml_file: PathBuf,
    short_names: bool,
) -> PyResult<&PyDict> {
    validate_file(&xml_file)?;
    let data = parse_xml_pandas(py, &xml_file, short_names)?;

    Ok(data)
}

#[pymodule]
fn _prelude_parser(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(_parse_flat_file_to_dict, m)?)?;
    m.add_function(wrap_pyfunction!(_parse_flat_file_to_pandas_dict, m)?)?;
    m.add("FileNotFoundError", py.get_type::<FileNotFoundError>())?;
    m.add(
        "InvalidFileTypeError",
        py.get_type::<InvalidFileTypeError>(),
    )?;
    m.add("ParsingError", py.get_type::<ParsingError>())?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::assert_eq;

    use super::*;

    #[test]
    fn test_to_snake() {
        assert_eq!(
            to_snake("i_communications_Details"),
            String::from("i_communications_details")
        );
    }
}
