"""SysOverview command-line entry point."""

import time

from sysoverview.battery.stats import (
    get_battery_health_percentage,
    get_battery_stats,
    get_battery_temperature,
)
from sysoverview.cpu.stats import (
    get_core_count,
    get_core_temperatures,
    get_cpu_frequency,
    get_cpu_temperature,
    get_cpu_usage,
    get_load_average,
    get_per_core_usage,
    prime_cpu_usage,
)
from sysoverview.memory.stats import get_memory_stats, get_swap_stats
from sysoverview.storage.stats import (
    get_filesystem_type,
    get_mounted_storage,
    get_storage_stats,
)


def _format_duration(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, remaining_seconds = divmod(remainder, 60)

    if hours:
        return f"{hours}h {minutes}m"
    if minutes:
        return f"{minutes}m"
    return f"{remaining_seconds}s"


def main() -> None:
    """Display a snapshot of the laptop's system statistics."""
    prime_cpu_usage()
    time.sleep(1)

    gib = 1024**3
    cpu_usage = get_cpu_usage()
    physical_cores, logical_cpus = get_core_count()
    per_core_usage = get_per_core_usage()
    core_temperatures = get_core_temperatures()
    frequency = get_cpu_frequency()
    load_1, load_5, load_15 = get_load_average()
    temperature = get_cpu_temperature()
    memory = get_memory_stats()
    swap = get_swap_stats()
    storage = get_storage_stats()
    filesystem_type = get_filesystem_type()
    mounted_storage = [
        mounted for mounted in get_mounted_storage() if mounted.mount_point != "/"
    ]
    battery = get_battery_stats()
    battery_health = get_battery_health_percentage()
    battery_temperature = get_battery_temperature()

    print("SysOverview")
    print(f"CPU usage: {cpu_usage}%")
    print(f"Physical cores: {physical_cores}")
    print(f"Logical CPUs: {logical_cpus}")
    print(f"CPU frequency: {frequency}")

    if temperature is None:
        print("CPU temperature: unavailable")
    else:
        print(f"CPU temperature: {temperature:.1f}°C")

    print("Physical core temperatures:")
    if core_temperatures:
        for core_temperature in core_temperatures:
            print(f"  {core_temperature.label}: {core_temperature.current:.1f}°C")
    else:
        print("  Unavailable")

    print(f"Load average: 1 min: {load_1}, 5 min: {load_5}, 15 min: {load_15}")
    print("Per-core usage:")

    for core_number, core_usage in enumerate(per_core_usage, start=1):
        print(f"  Core {core_number}: {core_usage}%")

    print("Memory:")
    print(f"  Used: {memory.used / gib:.2f} / {memory.total / gib:.2f} GiB")
    print(f"  Available: {memory.available / gib:.2f} GiB")
    print(f"  Usage: {memory.percentage}%")

    print("Swap:")
    if swap.total == 0:
        print("  Disabled")
    else:
        print(f"  Used: {swap.used / gib:.2f} / {swap.total / gib:.2f} GiB")
        print(f"  Free: {swap.free / gib:.2f} GiB")
        print(f"  Usage: {swap.percentage}%")

    print("Battery:")
    if battery is None:
        print("  Not detected")
    else:
        print(f"  Charge: {battery.percent:.1f}%")
        power_status = "Plugged in" if battery.is_plugged_in else "On battery"
        print(f"  Power: {power_status}")

        if battery.seconds_remaining is None:
            print("  Time remaining: unavailable")
        else:
            print(f"  Time remaining: {_format_duration(battery.seconds_remaining)}")

        if battery_health is None:
            print("  Health: unavailable")
        else:
            print(f"  Health: {battery_health:.1f}%")

        if battery_temperature is None:
            print("  Temperature: unavailable")
        else:
            print(f"  Temperature: {battery_temperature:.1f}°C")

    print("Storage (/):")
    print(f"  Filesystem: {filesystem_type or 'Unavailable'}")
    print(f"  Used: {storage.used / gib:.2f} / {storage.total / gib:.2f} GiB")
    print(f"  Free: {storage.free / gib:.2f} GiB")
    print(f"  Usage: {storage.percentage}%")

    print("Other mounted filesystems:")
    if mounted_storage:
        for mounted in mounted_storage:
            print(f"  {mounted.device} at {mounted.mount_point} ({mounted.fstype})")
            print(
                f"    Used: {mounted.used / gib:.2f} / "
                f"{mounted.total / gib:.2f} GiB ({mounted.percentage}%)"
            )
    else:
        print("  None")
