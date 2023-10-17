use std::error::Error;
use std::fs::File;
use std::io::Write;
use std::path::PathBuf;

use crate::io::extract_regions_from_bed_file;
use crate::models::region::Region;
use crate::models::universe::Universe;

pub struct RegionSet {
    pub regions: Vec<Region>,
    curr: usize,
}

impl TryFrom<PathBuf> for RegionSet {
    type Error = Box<dyn Error>;

    fn try_from(value: PathBuf) -> Result<Self, Self::Error> {
        let regions = extract_regions_from_bed_file(&value)?;
        Ok(RegionSet { regions, curr: 0 })
    }
}

impl From<Vec<Region>> for RegionSet {
    fn from(value: Vec<Region>) -> Self {
        let regions = value;
        RegionSet { regions, curr: 0 }
    }
}

impl Iterator for RegionSet {
    type Item = Region;

    fn next(&mut self) -> Option<Self::Item> {
        if self.curr < self.regions.len() {
            // do we need to clone? Is this a good idea? Is there a better way?
            let region = self.regions[self.curr].clone();
            self.curr += 1;
            Some(region)
        } else {
            None
        }
    }
}

impl<'a> IntoIterator for &'a RegionSet {
    type Item = &'a Region;
    type IntoIter = std::slice::Iter<'a, Region>;

    fn into_iter(self) -> Self::IntoIter {
        self.regions.iter()
    }
}

impl Clone for RegionSet {
    fn clone(&self) -> Self {
        let regions = self.regions.clone();
        RegionSet { regions, curr: 0 }
    }
}

pub struct TokenizedRegionSet<'a> {
    pub regions: Vec<Region>,
    pub universe: &'a Universe,
}

impl<'a> IntoIterator for &'a TokenizedRegionSet<'_> {
    type Item = &'a Region;
    type IntoIter = std::slice::Iter<'a, Region>;

    fn into_iter(self) -> Self::IntoIter {
        self.regions.iter()
    }
}

impl<'a> TokenizedRegionSet<'a> {
    ///
    /// Create a new TokenizedRegionSet. the TokenizedRegionSet takes
    /// a reference to a Universe.
    ///
    /// # Arguments
    /// * `regions` - A vector of regions
    /// * `universe` - A reference to a Universe
    ///
    pub fn new(regions: Vec<Region>, universe: &'a Universe) -> Self {
        TokenizedRegionSet { regions, universe }
    }

    ///
    /// Write a TokenizedRegionSet to a BED file
    ///
    /// # Arguments
    /// * `path` - A PathBuf to write the BED file to
    ///
    pub fn to_bed_file(&self, path: &PathBuf) -> Result<(), Box<dyn Error>> {
        let mut file = File::create(path)?;
        for region in self.regions.iter() {
            let line = format!(
                "{}\t{}\t{}\n",
                region.chr.to_owned(),
                region.start,
                region.end
            );
            file.write_all(line.as_bytes())?;
        }
        Ok(())
    }

    ///
    /// Convert a TokenizedRegionSet to a vector of region IDs
    ///
    pub fn to_region_ids(&self) -> Vec<u32> {
        let mut region_ids = Vec::new();
        for region in &self.regions {
            region_ids.push(self.universe.convert_region_to_id(region));
        }
        region_ids
    }

    ///
    /// Convert a TokenizedRegionSet to a bit vector
    ///
    pub fn to_bit_vector(&self) -> Vec<bool> {
        let mut bit_vector = vec![false; self.universe.len() as usize];
        for region in self.regions.iter() {
            bit_vector[self.universe.convert_region_to_id(region) as usize] = true;
        }
        bit_vector
    }

    ///
    /// Convert a TokenizedRegionSet to a vector of one-hot vectors
    ///
    pub fn to_one_hot_vectors(&self) -> Vec<Vec<bool>> {
        let mut vectors = Vec::new();
        for region in self.regions.iter() {
            let mut bit_vector = vec![false; self.universe.len() as usize];
            bit_vector[self.universe.convert_region_to_id(region) as usize] = true;
            vectors.push(bit_vector);
        }
        vectors
    }
}

impl TokenizedRegionSet<'_> {
    pub fn len(&self) -> usize {
        self.regions.len()
    }

    pub fn is_empty(&self) -> bool {
        self.regions.is_empty()
    }
}