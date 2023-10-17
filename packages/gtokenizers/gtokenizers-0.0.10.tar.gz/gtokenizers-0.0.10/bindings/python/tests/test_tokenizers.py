import pytest

from gtokenizers import Region, TokenizedRegionSet, TreeTokenizer

@pytest.fixture
def vocab_file() -> str:
    return "tests/data/peaks.bed"



