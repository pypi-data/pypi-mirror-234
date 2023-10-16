# TODO: Eliminate dupe
from enum import Enum, IntEnum, unique, auto

class DataType(IntEnum):
    NONE = 0
    BOOL = 1
    INT8 = 2
    INT16 = 3
    INT32 = 4
    INT64 = 5

    FLOAT = 10
    DOUBLE = 11

    STRING = 20
    VARCHAR = 21
    JSON = 23
    BINARY_VECTOR = 100
    FLOAT_VECTOR = 101

    UNKNOWN = 999

@unique
class IndexType(str, Enum):
    FLAT = "FLAT"
    IVF_FLAT = "IVF_FLAT"
    IVF_SQ8 = "IVF_SQ8"
    IVF_PQ = "IVF_PQ"
    HNSW = "HNSW"
    ANNOY = "ANNOY"
    RHNSW_FLAT = "RHNSW_FLAT"
    RHNSW_PQ = "RHNSW_PQ"
    RHNSW_SQ = "RHNSW_SQ"

    # Binary Vectors
    BIN_FLAT = "BIN_FLAT"
    BIN_IVF_FLAT = "BIN_IVF_FLAT"


@unique
class VectorSpace(str, Enum):
    # for floating point vectors:
    L2 = "L2"
    IP = "IP"
    # for binary vectors:
    JACCARD = "JACCARD"
    TANIMOTO = "TANIMOTO"
    HAMMING = "HAMMING"
    SUPERSTRUCTURE = "SUPERSTRUCTURE"
    SUBSTRUCTURE = "SUBSTRUCTURE"

@unique
class HashAlgo(str, Enum):
    md5 = "md5"
    sha1 = "sha1"
    sha256 = "sha256"
    sha512 = "sha512"
    sha3_224 = "sha3_224"
    sha3_256 = "sha3_256"
    sha3_384 = "sha3_384"
    sha3_512 = "sha3_512"
    # TODO: Require length
    # shake_128 = "shake_128 "
    # shake_256 = "shake_256"
    blake2b = "blake2b"
    blake2s = "blake2s"
