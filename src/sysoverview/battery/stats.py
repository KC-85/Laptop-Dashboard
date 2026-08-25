"""Collect battery charge, health, temperature, and remaining-time data."""

from dataclasses import dataclass
from pathlib import Path

import psutil

POWER_SUPPLY_PATH = Path("/sys/class/power_supply")


@dataclass
class BatteryStats:
    percent: float
    seconds_remaining: int | None
    is_plugged_in: bool


def get_battery_stats() -> BatteryStats | None:
    battery = psutil.sensors_battery()
    if battery is None:
        return None

    seconds_remaining = battery.secsleft
    if seconds_remaining in (
        psutil.POWER_TIME_UNKNOWN,
        psutil.POWER_TIME_UNLIMITED,
    ):
        seconds_remaining = None

    return BatteryStats(
        percent=battery.percent,
        seconds_remaining=seconds_remaining,
        is_plugged_in=battery.power_plugged,
    )


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return None


def _read_int(path: Path) -> int | None:
    value = _read_text(path)
    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        return None


def _get_battery_path() -> Path | None:
    try:
        power_supplies = sorted(POWER_SUPPLY_PATH.iterdir())
    except OSError:
        return None

    for power_supply in power_supplies:
        if _read_text(power_supply / "type") == "Battery":
            return power_supply

    return None


def get_battery_temperature() -> float | None:
    """Return the battery temperature in degrees Celsius when available."""
    battery_path = _get_battery_path()
    if battery_path is None:
        return None

    temperature = _read_int(battery_path / "temp")
    if temperature is None:
        return None

    return temperature / 10


def get_battery_health_percentage() -> float | None:
    """Return full capacity as a percentage of design capacity."""
    battery_path = _get_battery_path()
    if battery_path is None:
        return None

    capacity_files = (
        ("energy_full", "energy_full_design"),
        ("charge_full", "charge_full_design"),
    )

    for full_name, design_name in capacity_files:
        full_capacity = _read_int(battery_path / full_name)
        design_capacity = _read_int(battery_path / design_name)

        if (
            full_capacity is not None
            and design_capacity is not None
            and full_capacity >= 0
            and design_capacity > 0
        ):
            return full_capacity / design_capacity * 100

    return None
