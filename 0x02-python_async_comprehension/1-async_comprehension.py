#!/usr/bin/env python3
"""
Import async_generator
"""
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    coroutine that takes no arguments
    """
    result = [i async for i in async_generator()]
    return result
