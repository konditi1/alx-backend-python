#!/usr/bin/env python3
"""
type notation for the function
"""
from typing import TypeVar, Mapping, Any, Union

K = TypeVar('K')
V = TypeVar('V', covariant=True)


def safely_get_value(dct: Mapping[K, V], key: K, default: Union[V, None] = None) -> Union[V, None]:
    """
    Return the value associated with the key in the mapping,
    or the default value if the key is not present.
    """
    if key in dct:
        return dct[key]
    else:
        return default
