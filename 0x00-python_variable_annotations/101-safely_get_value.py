#!/usr/bin/env python3
"""
Defines safely_get_value function
"""
from typing import Mapping, Any, Union, TypeVar


def safely_get_value(dct: Mapping,
                     key: Any,
                     default:
                     Union[TypeVar('T'),
                           None] = None) -> Union[Any, TypeVar('T')]:
    """
    Gets a value from a dict

    Args:
        dct: the dict

    Return:
        value from a dict related to key or None
    """
    if key in dct:
        return dct[key]
    else:
        return default
