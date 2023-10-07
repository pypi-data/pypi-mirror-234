"""
Modified from https://github.com/lebedov/msgpack-numpy
"""

import pickle
import sys

import numpy as np


def ndarray_to_bytes(obj):
    if obj.dtype == "O":
        return obj.dumps()
    if sys.platform == "darwin":
        return obj.tobytes()
    return obj.data if obj.flags["C_CONTIGUOUS"] else obj.tobytes()


def tostr(x):
    if isinstance(x, bytes):
        return x.decode()
    return str(x)


def numpy_encode(obj, chain=None):
    """
    Data encoder for serializing numpy data types.
    """

    if isinstance(obj, np.ndarray):
        # If the dtype is structured, store the interface description;
        # otherwise, store the corresponding array protocol type string:
        if obj.dtype.kind in ("V", "O"):
            kind = bytes(obj.dtype.kind, "ascii")
            descr = obj.dtype.descr
        else:
            kind = b""
            descr = obj.dtype.str

        return {
            b"nd": True,
            b"type": descr,
            b"kind": kind,
            b"shape": obj.shape,
            b"data": ndarray_to_bytes(obj),
        }
    elif isinstance(obj, (np.bool_, np.number)):
        return {b"nd": False, b"type": obj.dtype.str, b"data": obj.data}
    elif isinstance(obj, complex):
        return {b"complex": True, b"data": obj.__repr__()}
    else:
        return obj if chain is None else chain(obj)


def numpy_decode(obj, chain=None):
    """
    Decoder for deserializing numpy data types.
    """

    try:
        if b"nd" in obj:
            if obj[b"nd"] is True:
                # Check if b'kind' is in obj to enable decoding of data
                # serialized with older versions (#20) or data
                # that had dtype == 'O' (#46):
                if b"kind" in obj and obj[b"kind"] == b"V":
                    descr = [
                        tuple(tostr(t) if type(t) is bytes else t for t in d) for d in obj[b"type"]
                    ]
                elif b"kind" in obj and obj[b"kind"] == b"O":
                    return pickle.loads(obj[b"data"])
                else:
                    descr = obj[b"type"]
                return np.ndarray(
                    buffer=obj[b"data"], dtype=_unpack_dtype(descr), shape=obj[b"shape"]
                )
            else:
                descr = obj[b"type"]
                return np.frombuffer(obj[b"data"], dtype=_unpack_dtype(descr))[0]
        elif b"complex" in obj:
            return complex(tostr(obj[b"data"]))
        else:
            return obj if chain is None else chain(obj)
    except KeyError:
        return obj if chain is None else chain(obj)


def _unpack_dtype(dtype):
    """
    Unpack dtype descr, recursively unpacking nested structured dtypes.
    """

    if isinstance(dtype, (list, tuple)):
        # Unpack structured dtypes of the form: (name, type, *shape)
        dtype = [
            (subdtype[0], _unpack_dtype(subdtype[1])) + tuple(subdtype[2:]) for subdtype in dtype
        ]
    return np.dtype(dtype)
