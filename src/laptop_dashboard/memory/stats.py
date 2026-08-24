"""
This will show the memory stats of the system. It will show the total, used, free, and available memory in bytes.
It will also show the memory usage percentage and the swap memory stats.
The output will be in a human-readable format.
"""


from dataclasses import dataclass

import psutil


@dataclass
class MemoryStats:
    total: int
    used: int
    available: int
    percentage: float


@dataclass
class SwapStats:
    total: int
    used: int
    free: int
    percentage: float


def get_memory_stats() -> MemoryStats:
    mem = psutil.virtual_memory()

    return MemoryStats(
        total=mem.total,
        used=mem.used,
        available=mem.available,
        percentage=mem.percent,
    )


def get_swap_stats() -> SwapStats:
    swap = psutil.swap_memory()

    return SwapStats(
        total=swap.total,
        used=swap.used,
        free=swap.free,
        percentage=swap.percent,
    )
