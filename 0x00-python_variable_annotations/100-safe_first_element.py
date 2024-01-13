#!/usr/bin/env python
"""
Augment the following code with the correct duck-typed annotations:
"""


from typing import Any, Sequence, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Annotate the below function’s parameters and return values
    with the appropriate types
    """
    if lst:
        return lst[0]
    else:
        return None
