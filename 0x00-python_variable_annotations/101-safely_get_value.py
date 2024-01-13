#!/usr/bin/env python3
"""
type notation for the following function
"""
from typing import TypeVar, Dict, Optional

K = TypeVar('K')
V = TypeVar('V')


def safely_get_value(dct: Dict[K, V], key: K, default: Optional[V] = None) -> V:
    """
    Return the value associated with the key in the dictionary,
    or the default value if the key is not present.
    """
    if key in dct:
        return dct[key]
    else:
        return default
