use rust_lapper::{Interval, Lapper};
use std::collections::HashMap;
use std::path::Path;

use crate::models::region::Region;
use crate::models::region_set::{RegionSet, TokenizedRegionSet};
use crate::models::universe::Universe;
use crate::tokenizers::traits::Tokenizer;

pub mod traits;

///
/// A tokenizer that uses an interval tree to find overlaps
/// 
/// # Attributes
/// - `universe` - the universe of regions
/// - `tree` - the interval tree
/// 
/// # Methods
/// - `from` - create a new TreeTokenizer from a bed file
/// - `tokenize_region` - tokenize a region into the vocabulary of the tokenizer
/// - `tokenize_region_set` - tokenize a region set into the vocabulary of the tokenizer
/// - `tokenize_bed_set` - tokenize a bed set into the vocabulary of the tokenizer
/// - `unknown_token` - get the unknown token
pub struct TreeTokenizer {
    pub universe: Universe,
    pub tree: HashMap<String, Lapper<u32, u32>>,
}

impl From<&Path> for TreeTokenizer {

    /// 
    /// # Arguments
    /// - `value` - the path to the bed file
    /// 
    /// # Returns
    /// A new TreeTokenizer
    fn from(value: &Path) -> Self {
        let universe = Universe::from(value);
        let mut tree: HashMap<String, Lapper<u32, u32>> = HashMap::new();
        let mut intervals: HashMap<String, Vec<Interval<u32, u32>>> = HashMap::new();

        for region in universe.regions.iter() {
            // create interval
            let interval = Interval {
                start: region.start,
                stop: region.end,
                val: 0,
            };

            // use chr to get the vector of intervals
            let chr_intervals = intervals.entry(region.chr.clone()).or_insert(Vec::new());

            // push interval to vector
            chr_intervals.push(interval);
        }

        for (chr, chr_intervals) in intervals.iter() {
            let lapper: Lapper<u32, u32> = Lapper::new(chr_intervals.to_owned());
            tree.insert(chr.to_string(), lapper);
        }

        TreeTokenizer { universe, tree }
    }
}

impl Tokenizer for TreeTokenizer {
    ///
    /// # Arguments
    /// - `region` - the region to be tokenized
    /// 
    /// # Returns
    /// A TokenizedRegionSet that corresponds to one or more regions in the tokenizers vocab (or universe).
    /// 
    fn tokenize_region(&self, region: &Region) -> Option<TokenizedRegionSet> {
        // get the interval tree corresponding to that chromosome
        let tree = self.tree.get(&region.chr);

        // make sure the tree existed
        match tree {
            // give unknown token if it doesnt exist
            None => {
                let regions = vec![self.unknown_token()];
                Some(TokenizedRegionSet {
                    regions,
                    universe: &self.universe,
                })
            }

            // otherwise find overlaps
            Some(tree) => {
                let olaps: Vec<Region> = tree
                    .find(region.start, region.end)
                    .map(|interval| Region {
                        chr: region.chr.clone(),
                        start: interval.start,
                        end: interval.stop,
                    })
                    .collect();

                // if len is zero, return unknown token
                if olaps.is_empty() {
                    let regions = vec![self.unknown_token()];
                    return Some(TokenizedRegionSet {
                        regions,
                        universe: &self.universe,
                    });
                }

                Some(TokenizedRegionSet {
                    regions: olaps,
                    universe: &self.universe,
                })
            }
        }
    }

    fn tokenize_region_set(&self, region_set: &RegionSet) -> Option<TokenizedRegionSet> {
        let mut tokenized_regions: Vec<Region> = vec![];
        for region in region_set.into_iter() {
            let tree = self.tree.get(&region.chr);
            match tree {
                // give unknown token if they give a chromosome that doesnt exist
                None => tokenized_regions.push(self.unknown_token().to_owned()),

                // otherwise find overlaps
                Some(t) => {
                    // run the interval tree computation
                    let olaps = t
                        .find(region.start, region.end)
                        .map(|interval| Region {
                            chr: region.chr.clone(),
                            start: interval.start,
                            end: interval.stop,
                        })
                        .collect::<Vec<Region>>();

                    // check if there are overlaps
                    if olaps.is_empty() {
                        // no? give unknown token
                        tokenized_regions.push(self.unknown_token().to_owned());
                    } else {
                        // yes? add them to the tokenized regions
                        tokenized_regions.extend(olaps.iter().map(|i| Region {
                            chr: region.chr.clone(),
                            start: i.start,
                            end: i.end,
                        }));
                    }
                }
            }
        }
        Some(TokenizedRegionSet {
            regions: tokenized_regions,
            universe: &self.universe,
        })
    }
}
