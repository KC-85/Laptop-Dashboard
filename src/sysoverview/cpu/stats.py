"""
CPU Stats. This file contains functions to retrieve CPU statistics such as usage, frequency, temperature and load average.

To get the current CPU usage percentage.
This will return a float value representing the current CPU usage percentage.

To get the number of CPU cores.
This will return a tuple containing the number of physical CPU cores and logical CPU cores.

To get the CPU usage percentage for each core.
This will return a list containing the CPU usage percentage for each core.

To get the current CPU frequency.
This will return a CPUFrequency object containing the current, minimum, and maximum CPU frequency in MHz.

To get the CPU load average.
This will return a tuple containing the 1-minute, 5-minute, and 15-minute load averages.

To get the temperature of each physical CPU core.
This will return a list of CoreTemperature objects for the available core sensors.
"""

from dataclasses import dataclass

import psutil


def prime_cpu_usage() -> None:
    """Prime psutil's counters before non-blocking CPU usage polling."""
    psutil.cpu_percent(interval=None)
    psutil.cpu_percent(interval=None, percpu=True)


def get_cpu_usage() -> float:
    return psutil.cpu_percent(interval=None)


def get_core_count() -> tuple[int | None, int | None]:
    physical = psutil.cpu_count(logical=False)
    logical = psutil.cpu_count(logical=True)

    return physical, logical


def get_per_core_usage() -> list[float]:
    return psutil.cpu_percent(interval=None, percpu=True)


@dataclass
class CPUFrequency:
    current: float | None
    min: float | None
    max: float | None

    def __str__(self) -> str:
        return (
            f"Current: {self.current} MHz, "
            f"Min: {self.min} MHz, "
            f"Max: {self.max} MHz"
        )


def get_cpu_frequency() -> CPUFrequency:
    freq = psutil.cpu_freq()

    if freq is None:
        return CPUFrequency(current=None, min=None, max=None)

    return CPUFrequency(
        current=freq.current,
        min=freq.min,
        max=freq.max,
    )


def get_load_average() -> tuple[float, float, float]:
    return psutil.getloadavg()


def get_cpu_temperature() -> float | None:
    try:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            core_temps = temps["coretemp"]
            if core_temps:
                return core_temps[0].current
    except (AttributeError, KeyError):
        pass

    return None


@dataclass
class CoreTemperature:
    label: str
    current: float


def get_core_temperatures() -> list[CoreTemperature]:
    try:
        temps = psutil.sensors_temperatures()
    except AttributeError:
        return []

    return [
        CoreTemperature(label=reading.label, current=reading.current)
        for reading in temps.get("coretemp", [])
        if reading.label.startswith("Core ")
    ]
