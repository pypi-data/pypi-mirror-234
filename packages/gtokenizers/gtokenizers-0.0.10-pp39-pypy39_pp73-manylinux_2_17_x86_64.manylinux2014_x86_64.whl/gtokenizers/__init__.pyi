from typing import List

class Region:
    def __new__(cls, chr: str, start: int, end: int) -> Region: ...

    @property
    def chr(self) -> str: ...
    """
    Chromosome name. Sometimes called seqname.
    """

    @property
    def start(self) -> int: ...
    """
    Start position of the region.
    """

    @property
    def end(self) -> int: ...
    """
    End position of the region.
    """

    def __repr__(self) -> str: ...

class TokenizedRegionSet:
    def __new__(cls, regions: List[Region], bit_vector: List[bool], ids: List[int]): ...
    """
    Create a new TokenizedRegionSet.

    :param List[Region] regions: A list of regions.
    :param List[bool] bit_vector: A bit vector of the regions.
    :param List[int] ids: A list of ids.
    """

    def __init__(self, regions: List[Region], bit_vector: List[bool], ids: List[int]): ...
    """
    Create a new TokenizedRegionSet.

    :param List[Region] regions: A list of regions.
    :param List[bool] bit_vector: A bit vector of the regions.
    :param List[int] ids: A list of ids.
    """

    @property
    def regions(self) -> List[Region]: ...
    """
    A list of regions.
    """

    @property
    def bit_vector(self) -> List[bool]: ...
    """
    A bit vector of the regions. This is a list of booleans,
    where each boolean represents whether the region at the
    same index in the regions list is present in the set.
    """

    @property
    def ids(self) -> List[int]: ...
    """
    A list of ids. This is a list of integers, where each
    integer represents the index of the region in the regions
    list.
    """

    def __repr__(self) -> str: ...
    


class TreeTokenizer:
    def __new__(cls, path: str) -> TreeTokenizer: ...
    """
    Create a new TreeTokenizer from a bed file.

    :param str path: Path to a bed file.
    """

    def __init__(self, path: str) -> TreeTokenizer: ...
    """
    Create a new TreeTokenizer from a bed file.

    :param str path: Path to a bed file.
    """
    
    def __repr__(self) -> str: ...

    
    def tokenize(self, regions: List[Region]) -> TokenizedRegionSet: ...
    """
    Tokenize a list of regions into a TokenizedRegionSet. This
    tokenized region set can yield a list of regions, a bit vector, 
    or a list of ids.

    :param List[Region] regions: A list of regions to tokenize.
    """

    def encode_to_ids(self, regions: List[Region]) -> List[int]: ...
    """
    Encode a list of regions into a list of ids.

    :param List[Region] regions: A list of regions to encode.
    """

    def encode_to_bit_vector(self, regions: List[Region]) -> List[bool]: ...
    """
    Encode a list of regions into a bit vector.

    :param List[Region] regions: A list of regions to encode.
    """
