#!/usr/bin/env python3
"""
a type-annotated function zoom_array that takes a list of
integers named lst and an integer named factor as arguments
and returns a list of integers
"""
from typing import Tuple, List

from typing import Tuple, List


def zoom_array(lst: Tuple[int, ...], factor: int = 2) -> List[int]:
    """
    a type-annotated function zoom_array that takes a list of
    integers named lst and an integer named factor as arguments
    and returns a list of integers
    """
    zoomed_in: List[int] = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = (12, 72, 91)  # Use a tuple instead of a list for 'array'

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)  # Pass an integer instead of a float for 'factor'
