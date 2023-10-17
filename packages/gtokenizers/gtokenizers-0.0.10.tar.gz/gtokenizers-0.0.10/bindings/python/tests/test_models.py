import pytest

from gtokenizers import Region, TokenizedRegionSet

def test_region():
    r = Region("chr1", 100, 200)
    assert r.chr == "chr1"
    assert r.start == 100
    assert r.end == 200

def test_list_of_regions():
    r = Region("chr1", 100, 200)
    rlist = [r for _ in range(10)]
    assert all([r.chr == "chr1" for r in rlist])
    assert all([r.start == 100 for r in rlist])
    assert all([r.end == 200 for r in rlist])

def test_tokenized_region_set():
    r1 = Region("chr1", 100, 200)
    r2 = Region("chr2", 200, 300)
    r3 = Region("chr3", 300, 400)
    rlist = [r1, r2, r3]

    trs = TokenizedRegionSet(
        rlist,
        [True, True, True],
        [1, 2, 3]
    )
    assert trs.regions == rlist
    assert trs.bit_vector == [True, True, True]
    assert trs.ids == [1, 2, 3]