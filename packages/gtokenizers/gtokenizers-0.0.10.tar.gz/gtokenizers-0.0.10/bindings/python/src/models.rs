use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;
use pyo3::class::basic::CompareOp;


#[pyclass(name="Region")]
#[derive(Clone, Debug)]
pub struct PyRegion {
    pub chr: String,
    pub start: u32,
    pub end: u32
}

#[pymethods]
impl PyRegion {
    #[new]
    pub fn new(chr: String, start: u32, end: u32) -> Self {
        PyRegion {
            chr,
            start,
            end
        }
    }

    #[getter]
    pub fn chr(&self) -> PyResult<&str> {
        Ok(&self.chr)
    }

    #[getter]
    pub fn start(&self) -> PyResult<u32> {
        Ok(self.start)
    }

    #[getter]
    pub fn end(&self) -> PyResult<u32> {
        Ok(self.end)
    }
    pub fn __repr__(&self) -> String {
        format!("Region({}, {}, {})", self.chr, self.start, self.end)
    }

    pub fn __richcmp__(&self, other: PyRef<PyRegion>, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Eq => Ok(self.chr == other.chr && self.start == other.start && self.end == other.end),
            CompareOp::Ne => Ok(self.chr != other.chr || self.start != other.start || self.end != other.end),
            _ => Err(PyTypeError::new_err("Unsupported comparison operator"))
        }
    }
}

#[pyclass(name="TokenizedRegionSet")]
#[derive(Clone, Debug)]
pub struct PyTokenizedRegionSet {
    pub regions: Vec<PyRegion>,
    pub bit_vector: Vec<bool>,
    pub ids: Vec<u32>,
}

#[pymethods]
impl PyTokenizedRegionSet {
    #[new]
    pub fn new(regions: Vec<PyRegion>, bit_vector: Vec<bool>, ids: Vec<u32>) -> Self {
        PyTokenizedRegionSet {
            regions,
            bit_vector,
            ids
        }
    }

    #[getter]
    pub fn regions(&self) -> PyResult<Vec<PyRegion>> {
        Ok(self.regions.to_owned())
    }
    #[getter]
    pub fn bit_vector(&self) -> PyResult<Vec<bool>> {
        Ok(self.bit_vector.clone())
    }
    #[getter]
    pub fn ids(&self) -> PyResult<Vec<u32>> {
        Ok(self.ids.clone())
    }

    pub fn __repr__(&self) -> String {
        format!("TokenizedRegionSet({} regions)", self.regions.len())
    }
}