#!/usr/bin/env python3
"""
 Async routine that spawns wait_random n times with the specified max_delay.
"""
import asyncio
from typing import List

wait_random = __import__(
    '0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int = 10) -> List[float]:
    """
    Async routine that spawns wait_random n times with the specified max_delay.

    Args:
        n (int): Number of times to spawn wait_random.
        max_delay (int): Maximum delay in seconds (default is 10).

    Returns:
        List[float]: List of delays in ascending order.
    """
    delays = []

    async def append_delay(delay: float):
        delays.append(delay)

    tasks = [wait_random(max_delay).then(append_delay) for _ in range(n)]

    await asyncio.gather(*tasks)

    return sorted(delays)
