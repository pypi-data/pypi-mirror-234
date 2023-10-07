import builtins
import inspect
from typing import Callable, List


def dtype_to_str(dtype: type) -> str:
    """
    Convert a dtype to a string.

    Args:
        dtype (type): Data type

    Returns:
        str: String representation of the data type
    """
    return dtype.__name__


def str_to_dtype(dtype: str) -> type:
    """
    Convert a string to a dtype.

    Args:
        dtype (str): String representation of the data type

    Returns:
        type: Data type
    """
    if dtype == "_empty":
        return inspect._empty
    return builtins.__dict__.get(dtype)


def signature_to_dict(func: Callable, include_class_obj=False) -> dict:
    """
    Convert a function signature to a dictionary.
    The dictionary can be used to reconstruct the signature using dict_to_signature.

    Args:
        func (Callable): Function to be converted

    Returns:
        dict: Dictionary representation of the function signature
    """
    out = []
    params = inspect.signature(func).parameters
    for param_name, param in params.items():
        if not include_class_obj and param_name == "self" or param_name == "cls":
            continue
        out.append(
            {
                "name": param_name,
                "kind": param.kind.name,
                "default": param.default if param.default != inspect._empty else "_empty",
                "annotation": dtype_to_str(param.annotation),
            }
        )
    return out


def dict_to_signature(params: List[dict]) -> inspect.Signature:
    """
    Convert a dictionary representation of a function signature to a signature object.

    Args:
        params (List[dict]): List of dictionaries representing the function signature

    Returns:
        inspect.Signature: Signature object
    """
    out = []
    for param in params:
        out.append(
            inspect.Parameter(
                name=param["name"],
                kind=getattr(inspect.Parameter, param["kind"]),
                default=param["default"] if param["default"] != "_empty" else inspect._empty,
                annotation=str_to_dtype(param["annotation"]),
            )
        )
    return inspect.Signature(out)
