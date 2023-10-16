use gtokenizers::tokenizers::traits::Tokenizer;
use pyo3::prelude::*;
use pyo3::types::PyList;

use std::path::Path;

use gtokenizers::tokenizers::TreeTokenizer;
use gtokenizers::models::region_set::RegionSet;
use gtokenizers::models::region::Region;

use crate::models::{PyTokenizedRegionSet, PyRegion};

#[pyclass(name = "TreeTokenizer")]
pub struct PyTreeTokenizer {
    pub tokenizer: TreeTokenizer,
}

#[pymethods]
impl PyTreeTokenizer {
    #[new]
    pub fn new(path: String) -> Self {
        let path = Path::new(&path);
        let tokenizer = TreeTokenizer::from(path);

        PyTreeTokenizer { 
            tokenizer
        }
    }

    pub fn __len__(&self) -> usize {
        self.tokenizer.universe.len() as usize
    }

    pub fn __repr__(&self) -> String {
        format!("TreeTokenizer({} total regions)", self.tokenizer.universe.len())
    }

    pub fn tokenize(&self, regions: &PyList) -> PyResult<PyTokenizedRegionSet> {
        
        // attempt to map the list to a vector of regions
        let regions = regions.iter().map(|x| {
            
            // extract chr, start, end
            // this lets us interface any python object with chr, start, end attributes
            let chr = x.getattr("chr").unwrap().extract::<String>().unwrap();
            let start = x.getattr("start").unwrap().extract::<u32>().unwrap();
            let end = x.getattr("end").unwrap().extract::<u32>().unwrap();
            
            Region {
                chr,
                start,
                end
            }

        }).collect::<Vec<_>>();

        // create RegionSet
        let rs = RegionSet::from(regions);
        
        // tokenize
        let tokenized_regions = self.tokenizer.tokenize_region_set(&rs);

        // create pytokenizedregionset
        let tokenized_regions = match tokenized_regions {
            Some(tokenized_regions) => {
                let regions = tokenized_regions.regions.iter().map(|x| {
                    PyRegion::new(x.chr.clone(), x.start, x.end)
                }).collect::<Vec<_>>();
                let bit_vector = tokenized_regions.to_bit_vector();
                let ids = tokenized_regions.to_region_ids();
                Ok(PyTokenizedRegionSet::new(regions, bit_vector, ids))
            },
            // return error if tokenized_regions is None
            None => {
                return Err(pyo3::exceptions::PyValueError::new_err("Failed to tokenize regions"))
            }
        };

        tokenized_regions
        
    }
}