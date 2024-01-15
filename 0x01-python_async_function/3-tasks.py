#!/usr/bin/env python3
"""
 Returns an asyncio.Task for wait_random with the specified max_delay.
"""
import asyncio
from typing import Callable

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Returns an asyncio.Task for wait_random with the specified max_delay.

    Args:
        max_delay (int): Maximum delay in seconds.

    Returns:
        asyncio.Task: Task representing the execution of wait_random.
    """
    return asyncio.create_task(wait_random(max_delay))
