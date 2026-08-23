"""
This module contains unit tests for the CPU statistics functionality in the laptop dashboard application.
The tests cover various scenarios to ensure accurate data collection and processing of CPU metrics.
"""


from types import SimpleNamespace
from unittest.mock import patch

from laptop_dashboard.cpu import stats


def test_get_cpu_usage():
    with patch("psutil.cpu_percent", return_value=42.0):
        assert stats.get_cpu_usage() == 42.0


def test_get_core_count():
    with patch("psutil.cpu_count", side_effect=[4, 8]):
        physical, logical = stats.get_core_count()
        assert physical == 4
        assert logical == 8
