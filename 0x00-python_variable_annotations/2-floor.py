#!/usr/bin/env python3
"""
a type-annotated function floor that takes a float n as argument
and returns the floor of the float.
"""
from math import floor as math_floor


def floor(n: float) -> int:
    """
    a type-annotated function floor that takes a float n as argument
    and returns the floor of the float.
    """
    return math_floor(n)
