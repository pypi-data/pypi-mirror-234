from http import HTTPStatus
import tempfile
import requests
import numpy as np
from typing import BinaryIO, List, Any, Union
import io, os
from .models.collection_schema import CollectionSchema
from .models.field_schema import FieldSchema
from .lectric_types import DataType


def create_random_vectors(nvects: int, dim: int) -> List[List[float]]:
    return [np.random.rand(dim).tolist() for _ in range(nvects)]

def check_ok(resp: requests.Response):
    if resp.status_code != HTTPStatus.OK:
        raise RuntimeError(resp.json())

def is_file_like(obj: Any) -> bool:
    """Does the object appear to be a file?

    Args:
        obj (Any): The object in question

    Returns:
        [bool]: True if is file like else False
    """
    return isinstance(obj, io.TextIOBase) or \
                isinstance(obj, io.BufferedIOBase) or \
                isinstance(obj, io.RawIOBase) or \
                isinstance(obj, io.IOBase)


def to_tmpfile(_input: bytes) -> BinaryIO:
    """Write a sequence of bytes a temporary file

    Args:
        _input (bytes): The data to be written to temp file

    Returns:
        [BinaryIO]: The temporary file that is closed when garbage collectede
    """
    fp = tempfile.TemporaryFile()
    fp.write(_input)
    fp.seek(0)
    return fp


def get_tmp_file(file: Union[str, bytes, BinaryIO]) -> BinaryIO:
    if is_file_like(file):
        tmp_file = file
    elif isinstance(file, str):
        if not os.path.exists(file):
            raise RuntimeError("`file` arg as str must be the path to file")
        tmp_file = open(file, "rb")

    elif isinstance(file, bytes): # Assume encoded JPG
        tmp_file = to_tmpfile(file)
    else:
        raise RuntimeError("Unable to process `file` argument, unsupported input type")

    return tmp_file

def pformat_field_schema(fschema: FieldSchema) -> str:
    desc = "" if not fschema.description else f"Description: {fschema.description}"
    dim = "" if not fschema.dim else f"Dim: {fschema.dim}"
    max_len = "" if not fschema.max_length else f"Max length: {fschema.max_length}"
    s =  f"""
            FieldSchema:
                Name: {fschema.name}
                {desc}
                Type: {DataType(fschema.dtype)}
                Primary key: {fschema.is_primary}
                Auto ID: {bool(fschema.auto_id)}
                {dim}
                {max_len}
        """.rstrip()

    return s

def pformat_collection_schema(cschema: CollectionSchema) -> str:
    schema_str: str = "\nCollectionSchema:"
    schema_str += "" if not cschema.description else f"\n\tDescription: {cschema.description}"
    for field in cschema.fields:
        field_str = pformat_field_schema(field)
        schema_str += field_str
    return schema_str
