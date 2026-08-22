"""Laptop Dashboard command-line entry point."""

from laptop_dashboard.cpu.stats import (
    get_core_count,
    get_cpu_frequency,
    get_cpu_usage,
    get_load_average,
    get_per_core_usage,
)


def main() -> None:
    """Display a snapshot of the laptop's CPU statistics."""
    cpu_usage = get_cpu_usage()
    physical_cores, logical_cpus = get_core_count()
    per_core_usage = get_per_core_usage()
    frequency = get_cpu_frequency()
    load_1, load_5, load_15 = get_load_average()

    print("Laptop Dashboard")
    print(f"CPU usage: {cpu_usage}%")
    print(f"Physical cores: {physical_cores}")
    print(f"Logical CPUs: {logical_cpus}")
    print(f"CPU frequency: {frequency}")
    print(f"Load average: 1 min: {load_1}, 5 min: {load_5}, 15 min: {load_15}")
    print("Per-core usage:")

    for core_number, core_usage in enumerate(per_core_usage, start=1):
        print(f"  Core {core_number}: {core_usage}%")
