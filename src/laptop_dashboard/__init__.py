"""Laptop Dashboard command-line entry point."""

import time

from laptop_dashboard.cpu.stats import (
    get_core_count,
    get_core_temperatures,
    get_cpu_frequency,
    get_cpu_temperature,
    get_cpu_usage,
    get_load_average,
    get_per_core_usage,
    prime_cpu_usage,
)
from laptop_dashboard.memory.stats import get_memory_stats, get_swap_stats


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

    print("Laptop Dashboard")
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
