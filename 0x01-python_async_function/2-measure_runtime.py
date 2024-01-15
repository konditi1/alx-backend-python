#!/usr/bin/env python3
import asyncio
import time
"""
Measures total execution time for wait_n(n, max_delay)returns total_time / n.
"""
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Measure total execution time for wait_n(n, max_delay)return total_time / n.

    Args:
        n (int): Number of times to spawn wait_random.
        max_delay (int): Maximum delay in seconds.

    Returns:
        float: Average execution time per wait_random call.
    """
    start_time = time.time()
    asyncio.run(wait_n(n, max_delay))
    end_time = time.time()

    total_time = end_time - start_time
    return total_time / n
