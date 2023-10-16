use std::{collections::HashMap, path::Path};

use crate::io::extract_regions_from_bed_file;
use crate::models::region::Region;
use crate::tokenizers::traits::{UNKNOWN_CHR, UNKNOWN_END, UNKNOWN_START};

fn generate_region_to_id_map(regions: &[Region]) -> HashMap<Region, u32> {
    let mut current_id = 0;
    let mut region_to_id: HashMap<Region, u32> = HashMap::new();
    for region in regions.iter() {
        region_to_id.entry(region.to_owned()).or_insert_with(|| {
            let old_id = current_id;
            current_id += 1;
            old_id
        });
    }

    region_to_id
}

pub struct Universe {
    pub regions: Vec<Region>,
    pub region_to_id: HashMap<Region, u32>,
    length: u32
}

impl Universe {
    pub fn convert_region_to_id(&self, region: &Region) -> u32 {
        let id = self.region_to_id.get(region);
        match id {
            Some(id) => id.to_owned(),
            None => self
                .region_to_id
                .get(&Region {
                    chr: UNKNOWN_CHR.to_string(),
                    start: UNKNOWN_START as u32,
                    end: UNKNOWN_END as u32,
                })
                .unwrap()
                .to_owned(),
        }
    }

    pub fn len(&self) -> u32 {
        self.length
    }

    pub fn is_empty(&self) -> bool {
        self.length == 0
    }
}

impl From<Vec<Region>> for Universe {
    fn from(value: Vec<Region>) -> Self {

        // create the region to id map and add the Unk token if it doesn't exist
        let mut region_to_id = generate_region_to_id_map(&value);
        let total_regions = region_to_id.len();

        // add Unk token if it doesn't exist
        // its possible the vocab file passed
        // in does have the Unk token, but
        // we don't know that here
        let unk = Region {
            chr: UNKNOWN_CHR.to_string(),
            start: UNKNOWN_START as u32,
            end: UNKNOWN_END as u32,
        };
        
        // add the Unk token to the region to id map
        region_to_id.entry(unk).or_insert(total_regions as u32);
        
        Universe {
            regions: value,
            region_to_id,
            length: (total_regions + 1) as u32 // increment by 1 to account for the Unk token
        }
    }
}

impl From<&Path> for Universe {
    fn from(value: &Path) -> Self {
        let regions = extract_regions_from_bed_file(value);

        let regions = match regions {
            Ok(r) => r,
            // should probably change this to something else,
            // but couldn't figure out how to return a `Result`
            // from a trait implementation
            Err(e) => panic!("{e}"),
        };

        let mut region_to_id = generate_region_to_id_map(&regions);
        let total_regions = region_to_id.len();

        // add Unk token if it doesn't exist
        // its possible the vocab file passed
        // in does have the Unk token, but
        // we don't know that here
        let unk = Region {
            chr: UNKNOWN_CHR.to_string(),
            start: UNKNOWN_START as u32,
            end: UNKNOWN_END as u32,
        };
        
        // add the Unk token to the region to id map
        // dont need to bump since index will be equal to the current number of regions
        // this is becuase the index starts at 0
        region_to_id.entry(unk).or_insert(total_regions as u32);
        let total_regions = region_to_id.len();
        
        Universe {
            regions,
            region_to_id,
            length: total_regions as u32
        }
    }
}