"""
This module contains unit tests for the memory statistics functionality in the laptop dashboard application.
The tests cover various scenarios to ensure accurate data collection and processing of memory metrics.
"""

from types import SimpleNamespace
from unittest.mock import patch

from laptop_dashboard.memory import stats


def test_get_memory_stats() -> None:
    mock_mem = SimpleNamespace(
        total=8 * 1024**3,  # 8 GiB
        used=4 * 1024**3,   # 4 GiB
        available=6 * 1024**3,  # 6 GiB
        percent=50.0,
    )
    with patch.object(stats.psutil, "virtual_memory", return_value=mock_mem):
        mem_stats = stats.get_memory_stats()
        assert mem_stats.total == 8 * 1024**3
        assert mem_stats.used == 4 * 1024**3
        assert mem_stats.available == 6 * 1024**3
        assert mem_stats.percentage == 50.0


def test_get_swap_stats() -> None:
    mock_swap = SimpleNamespace(
        total=2 * 1024**3,  # 2 GB
        used=1 * 1024**3,   # 1 GB
        free=1 * 1024**3,   # 1 GB
        percent=50.0,
    )
    with patch.object(stats.psutil, "swap_memory", return_value=mock_swap):
        swap_stats = stats.get_swap_stats()
        assert swap_stats.total == 2 * 1024**3
        assert swap_stats.used == 1 * 1024**3
        assert swap_stats.free == 1 * 1024**3
        assert swap_stats.percentage == 50.0


def test_get_no_swap() -> None:
    mock_swap = SimpleNamespace(
        total=0,  # No swap
        used=0,
        free=0,
        percent=0.0,
    )
    with patch.object(stats.psutil, "swap_memory", return_value=mock_swap):
        swap_stats = stats.get_swap_stats()
        assert swap_stats.total == 0
        assert swap_stats.used == 0
        assert swap_stats.free == 0
        assert swap_stats.percentage == 0.0
