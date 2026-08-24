"""
Collect system memory and swap statistics.

Memory statistics include total, used, and available RAM in bytes,
along with the usage percentage. Swap statistics include total,
used, and free swap in bytes, along with the usage percentage.

Human-readable formatting is handled by the presentation layer.
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
