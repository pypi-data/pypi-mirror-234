use crate::models::universe::Universe;

#[derive(Debug, Eq, Hash, PartialEq)]
pub struct Region {
    pub chr: String,
    pub start: u32,
    pub end: u32,
}

pub type TokenizedRegions = Vec<Region>;

impl Clone for Region {
    fn clone(&self) -> Self {
        Region {
            chr: self.chr.clone(),
            start: self.start,
            end: self.end,
        }
    }
}

pub struct TokenizedRegion<'a> {
    pub universe: &'a Universe,
    pub chr: String,
    pub start: u32,
    pub end: u32,
    pub region: Region,
}

impl TokenizedRegion<'_> {
    pub fn to_id(&self) -> u32 {
        self.universe.convert_region_to_id(&self.region)
    }
    pub fn to_bit_vector(&self) -> Vec<bool> {
        let mut bit_vector = vec![false; self.universe.regions.len()];
        bit_vector[self.universe.convert_region_to_id(&self.region) as usize] = true;
        bit_vector
    }
    pub fn to_one_hot_encoded(&self) -> Vec<u8> {
        let mut bit_vector = vec![0; self.universe.regions.len()];
        bit_vector[self.universe.convert_region_to_id(&self.region) as usize] = 1;
        bit_vector
    }
}
