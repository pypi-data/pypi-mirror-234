use gtokenizers::models::{region::Region, region_set::RegionSet};

#[test]
fn init_region() {
    let r = Region {
        chr: "chr1".to_string(),
        start: 100,
        end: 200,
    };
    assert_eq!(r.chr, "chr1");
    assert_eq!(r.start, 100);
    assert_eq!(r.end, 200);
}

#[test]
fn init_region_set_from_file() {
    let file = std::path::PathBuf::from("tests/data/peaks.bed");
    let rs = RegionSet::try_from(file);
    assert!(rs.is_ok());
}

#[test]
fn init_region_set_from_vec() {
    let r = Region {
        chr: "chr1".to_string(),
        start: 100,
        end: 200,
    };
    let rs = RegionSet::from(vec![r]);
    assert_eq!(rs.regions.len(), 1);
}
