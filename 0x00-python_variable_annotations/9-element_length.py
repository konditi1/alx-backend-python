#!/usr/bin/env python3
"""
Annotate the below function’s parameters and return values with the
appropriate types
"""

from typing import List


def element_length(lst: list) -> List[tuple]:
    """
    Annotate the below function’s parameters and return values with the
    appropriate types
    """
    return [(i, len(i)) for i in lst]
