use gtokenizers::tokenizers::traits::Tokenizer;
use gtokenizers::tokenizers::TreeTokenizer;
use gtokenizers::models::region::Region;
use std::path::Path;

#[test]
fn test_make_tokenizer() {
    let bed_file = Path::new("tests/data/peaks.bed");
    let tokenizer = TreeTokenizer::from(bed_file);

    // make sure the tree got made, and the universe is there, check for unknown token
    assert_eq!(tokenizer.tree.len(), 23); // 23 chromosomes
    assert_eq!(tokenizer.universe.regions.len(), 6551); // 6551 regions
    assert_eq!(tokenizer.universe.region_to_id.len(), 6552); // 6551 regions + 1 unknown token
}


#[test]
fn test_universe_len() {
    let bed_file = Path::new("tests/data/peaks.bed");
    let tokenizer = TreeTokenizer::from(bed_file);

    assert_eq!(tokenizer.universe.len(), 6552); // 6551 regions + 1 unknown token
}

#[test]
fn test_tokenize_region() {
    let bed_file = Path::new("tests/data/peaks.bed");
    let tokenizer = TreeTokenizer::from(bed_file);
    // chr1	151399431	151399527
    let region = Region {
        chr: "chr1".to_string(),
        start: 151399383,
        end: 151399479,
    };

    let tokenized_regions = tokenizer.tokenize_region(&region);
    let tokenized_regions = tokenized_regions.unwrap();
    assert_eq!(tokenized_regions.len(), 1);
    assert_eq!(tokenized_regions.regions[0].chr, "chr1");
    assert_eq!(tokenized_regions.regions[0].start, 151399431);
    assert_eq!(tokenized_regions.regions[0].end, 151399527);
}

#[test]
fn test_convert_to_bit_vector() {
    let bed_file = Path::new("tests/data/peaks.bed");
    let tokenizer = TreeTokenizer::from(bed_file);

    // chr1	151399431	151399527
    let region = Region {
        chr: "chr1".to_string(),
        start: 151399383,
        end: 151399479,
    };

    let tokenized_regions = tokenizer.tokenize_region(&region);
    let tokenized_regions = tokenized_regions.unwrap();

    let bit_vector = tokenized_regions.to_bit_vector();
    assert_eq!(bit_vector.len(), 6552);
    assert!(!bit_vector[0]); // should be false
    assert!(bit_vector[6]); // should be true
    assert!(!bit_vector[6551]); // should be false
}

#[test]
fn test_get_unknown_region() {
    let bed_file = Path::new("tests/data/peaks.bed");
    let tokenizer = TreeTokenizer::from(bed_file);

    // chr1	151399431	151399527
    let region = Region {
        chr: "chr1".to_string(),
        start: 10,
        end: 11,
    };

    let tokenized_regions = tokenizer.tokenize_region(&region);
    let tokenized_regions = tokenized_regions.unwrap();

    assert_eq!(tokenized_regions.len(), 1);
    assert_eq!(tokenized_regions.regions[0].chr, "chrUNK");
    assert_eq!(tokenized_regions.regions[0].start, 0);
    assert_eq!(tokenized_regions.regions[0].end, 0);
}

#[test]
fn test_get_unknown_region_bit_vector() {

    let bed_file = Path::new("tests/data/peaks.bed");
    let tokenizer = TreeTokenizer::from(bed_file);

    // chr1	151399431	151399527
    let region = Region {
        chr: "chr1".to_string(),
        start: 10,
        end: 11,
    };

    let tokenized_regions = tokenizer.tokenize_region(&region);
    let tokenized_regions = tokenized_regions.unwrap();

    let bit_vector = tokenized_regions.to_bit_vector();
    assert_eq!(bit_vector.len(), 6552);
    assert!(!bit_vector[0]); // should be false
    assert!(!bit_vector[6]); // should be false
    assert!(bit_vector[6551]); // should be true
}

#[test]
fn test_one_region_to_many_tokens() {

    let bed_file = Path::new("tests/data/peaks.bed");
    let tokenizer = TreeTokenizer::from(bed_file);

    // chr9	3526071	3526165
    // chr9	3526183	3526269
    let region = Region {
        chr: "chr9".to_string(),
        start: 3526051,
        end: 3526289,
    };

    let tokenized_regions = tokenizer.tokenize_region(&region);
    let tokenized_regions = tokenized_regions.unwrap();

    assert_eq!(tokenized_regions.len(), 2);
    assert_eq!(tokenized_regions.regions[0].chr, "chr9");
    assert_eq!(tokenized_regions.regions[0].start, 3526071);
    assert_eq!(tokenized_regions.regions[0].end, 3526165);
    assert_eq!(tokenized_regions.regions[1].chr, "chr9");
    assert_eq!(tokenized_regions.regions[1].start, 3526183);
    assert_eq!(tokenized_regions.regions[1].end, 3526269);


}

#[test]
fn test_one_region_to_many_tokens_as_bit_vector() {

    let bed_file = Path::new("tests/data/peaks.bed");
    let tokenizer = TreeTokenizer::from(bed_file);

    // chr9	3526071	3526165
    // chr9	3526183	3526269
    let region = Region {
        chr: "chr9".to_string(),
        start: 3526051,
        end: 3526289,
    };

    let tokenized_regions = tokenizer.tokenize_region(&region);
    let tokenized_regions = tokenized_regions.unwrap();
    let bit_vector = tokenized_regions.to_bit_vector();

    assert_eq!(bit_vector.len(), 6552);
    assert!(!bit_vector[0]); // should be false
    assert!(!bit_vector[9]); // should be false
    assert!(bit_vector[10]); // should be true
    assert!(bit_vector[11]); // should be true
    assert!(!bit_vector[13]); // should be false

}