"""Unit tests for battery statistics."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from sysoverview.battery import stats


def test_get_battery_stats() -> None:
    battery = SimpleNamespace(
        percent=75.0,
        secsleft=7200,
        power_plugged=False,
    )

    with patch.object(stats.psutil, "sensors_battery", return_value=battery):
        result = stats.get_battery_stats()

    assert result == stats.BatteryStats(
        percent=75.0,
        seconds_remaining=7200,
        is_plugged_in=False,
    )


def test_get_battery_stats_when_unavailable() -> None:
    with patch.object(stats.psutil, "sensors_battery", return_value=None):
        assert stats.get_battery_stats() is None


def test_get_battery_stats_with_unknown_time() -> None:
    battery = SimpleNamespace(
        percent=50.0,
        secsleft=stats.psutil.POWER_TIME_UNKNOWN,
        power_plugged=False,
    )

    with patch.object(stats.psutil, "sensors_battery", return_value=battery):
        result = stats.get_battery_stats()

    assert result == stats.BatteryStats(
        percent=50.0,
        seconds_remaining=None,
        is_plugged_in=False,
    )


def test_get_battery_stats_with_unlimited_time() -> None:
    battery = SimpleNamespace(
        percent=100.0,
        secsleft=stats.psutil.POWER_TIME_UNLIMITED,
        power_plugged=True,
    )

    with patch.object(stats.psutil, "sensors_battery", return_value=battery):
        result = stats.get_battery_stats()

    assert result == stats.BatteryStats(
        percent=100.0,
        seconds_remaining=None,
        is_plugged_in=True,
    )


def create_battery_directory(power_supply_path: Path) -> Path:
    battery_path = power_supply_path / "BAT0"
    battery_path.mkdir()
    (battery_path / "type").write_text("Battery\n", encoding="utf-8")
    return battery_path


def test_get_battery_temperature(tmp_path: Path) -> None:
    battery_path = create_battery_directory(tmp_path)
    (battery_path / "temp").write_text("315\n", encoding="utf-8")

    with patch.object(stats, "POWER_SUPPLY_PATH", tmp_path):
        assert stats.get_battery_temperature() == 31.5


def test_get_battery_temperature_when_unavailable(tmp_path: Path) -> None:
    create_battery_directory(tmp_path)

    with patch.object(stats, "POWER_SUPPLY_PATH", tmp_path):
        assert stats.get_battery_temperature() is None


def test_get_battery_health_from_charge_capacity(tmp_path: Path) -> None:
    battery_path = create_battery_directory(tmp_path)
    (battery_path / "charge_full").write_text("4000\n", encoding="utf-8")
    (battery_path / "charge_full_design").write_text("5000\n", encoding="utf-8")

    with patch.object(stats, "POWER_SUPPLY_PATH", tmp_path):
        assert stats.get_battery_health_percentage() == 80.0


def test_get_battery_health_from_energy_capacity(tmp_path: Path) -> None:
    battery_path = create_battery_directory(tmp_path)
    (battery_path / "energy_full").write_text("4500\n", encoding="utf-8")
    (battery_path / "energy_full_design").write_text("5000\n", encoding="utf-8")

    with patch.object(stats, "POWER_SUPPLY_PATH", tmp_path):
        assert stats.get_battery_health_percentage() == 90.0


def test_get_battery_health_when_unavailable(tmp_path: Path) -> None:
    create_battery_directory(tmp_path)

    with patch.object(stats, "POWER_SUPPLY_PATH", tmp_path):
        assert stats.get_battery_health_percentage() is None
