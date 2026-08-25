"""
This module contains unit tests for the CPU statistics functionality in SysOverview.
The tests cover various scenarios to ensure accurate data collection and processing of CPU metrics.
"""

from types import SimpleNamespace
from unittest.mock import call, patch

from sysoverview.cpu import stats


def test_prime_cpu_usage() -> None:
    with patch.object(stats.psutil, "cpu_percent") as mock_cpu_percent:
        stats.prime_cpu_usage()

    assert mock_cpu_percent.call_args_list == [
        call(interval=None),
        call(interval=None, percpu=True),
    ]


def test_get_cpu_usage():
    with patch("psutil.cpu_percent", return_value=42.0) as mock_cpu_percent:
        assert stats.get_cpu_usage() == 42.0
        mock_cpu_percent.assert_called_once_with(interval=None)


def test_get_core_count():
    with patch("psutil.cpu_count", side_effect=[4, 8]):
        physical, logical = stats.get_core_count()
        assert physical == 4
        assert logical == 8


def test_get_per_core_usage():
    with patch(
        "psutil.cpu_percent", return_value=[10.0, 20.0, 30.0, 40.0]
    ) as mock_cpu_percent:
        assert stats.get_per_core_usage() == [10.0, 20.0, 30.0, 40.0]
        mock_cpu_percent.assert_called_once_with(interval=None, percpu=True)


def test_get_cpu_frequency() -> None:
    mock_freq = SimpleNamespace(current=2500.0, min=1200.0, max=3500.0)
    with patch("psutil.cpu_freq", return_value=mock_freq):
        freq = stats.get_cpu_frequency()
        assert freq.current == 2500.0
        assert freq.min == 1200.0
        assert freq.max == 3500.0

def test_get_cpu_frequency_when_unavailable() -> None:
    with patch("psutil.cpu_freq", return_value=None):
        freq = stats.get_cpu_frequency()
        assert freq.current is None
        assert freq.min is None
        assert freq.max is None


def test_cpu_frequency_str() -> None:
    freq = stats.CPUFrequency(current=2500.0, min=1200.0, max=3500.0)
    expected_str = "Current: 2500.0 MHz, Min: 1200.0 MHz, Max: 3500.0 MHz"
    assert str(freq) == expected_str


def test_load_average():
    with patch("psutil.getloadavg", return_value=(0.5, 0.75, 1.0)):
        load_avg = stats.get_load_average()
        assert load_avg == (0.5, 0.75, 1.0)


def test_get_cpu_temperature() -> float | None:
    with patch("psutil.sensors_temperatures", return_value={"coretemp": [SimpleNamespace(current=55.0)]}):
        temp = stats.get_cpu_temperature()
        assert temp == 55.0

    with patch("psutil.sensors_temperatures", return_value={}):
        temp = stats.get_cpu_temperature()
        assert temp is None


def test_get_cpu_temperature_when_coretemp_unavailable() -> float | None:
    with patch("psutil.sensors_temperatures", return_value={"other": [SimpleNamespace(current=60.0)]}):
        temp = stats.get_cpu_temperature()
        assert temp is None


def test_get_core_temperatures() -> None:
    readings = [
        SimpleNamespace(label="Package id 0", current=55.0),
        SimpleNamespace(label="Core 0", current=53.0),
        SimpleNamespace(label="Core 1", current=51.0),
    ]

    with patch(
        "psutil.sensors_temperatures", return_value={"coretemp": readings}
    ):
        temperatures = stats.get_core_temperatures()

    assert temperatures == [
        stats.CoreTemperature(label="Core 0", current=53.0),
        stats.CoreTemperature(label="Core 1", current=51.0),
    ]


def test_get_core_temperatures_when_unavailable() -> None:
    with patch("psutil.sensors_temperatures", return_value={}):
        assert stats.get_core_temperatures() == []
