use pyo3::prelude::*;

pub mod tokenizers;
pub mod models;

use crate::tokenizers::PyTreeTokenizer;
use crate::models::{PyRegion, PyTokenizedRegionSet};

/// A Python module implemented in Rust.
#[pymodule]
fn gtokenizers(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyTreeTokenizer>()?;
    m.add_class::<PyRegion>()?;
    m.add_class::<PyTokenizedRegionSet>()?;
    Ok(())
}