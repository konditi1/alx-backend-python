#!/usr/bin/env python3
"""
Type-annotated function zoom_array that takes a list lst
and an integer factor as arguments and returns a list
"""
from typing import Tuple, List


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
    Type-annotated function zoom_array that takes a list lst
    and an integer factor as arguments and returns a list
    """
    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = (12, 72, 91)  # Use a tuple instead of a list for 'array'

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)  # Pass an integer instead of a float for 'factor'
