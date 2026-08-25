"""
Collect network traffic and interface statistics.

Network statistics include bytes and packets sent and received,
along with transmission errors and dropped packets. Interface
statistics include connection status, speed, MTU, and assigned
network addresses.

Raw values are returned by the collection layer. Human-readable
formatting and transfer-rate calculations are handled by the
presentation layer.
"""

from dataclasses import dataclass

import psutil


@dataclass
class NetworkTotals:
    bytes_sent: int
    bytes_received: int
    packets_sent: int
    packets_received: int
    errors_in: int
    errors_out: int
    dropped_in: int
    dropped_out: int


@dataclass
class NetworkAddress:
    family: int
    address: str
    netmask: str | None
    broadcast: str | None
    point_to_point: str | None


@dataclass
class NetworkInterface:
    name: str
    is_up: bool
    speed_mbps: int
    mtu: int
    addresses: list[NetworkAddress]


def get_network_totals() -> NetworkTotals:
    """Return cumulative system-wide network I/O counters."""
    counters = psutil.net_io_counters()

    return NetworkTotals(
        bytes_sent=counters.bytes_sent,
        bytes_received=counters.bytes_recv,
        packets_sent=counters.packets_sent,
        packets_received=counters.packets_recv,
        errors_in=counters.errin,
        errors_out=counters.errout,
        dropped_in=counters.dropin,
        dropped_out=counters.dropout,
    )


def get_network_interfaces() -> list[NetworkInterface]:
    """Return status and assigned addresses for each network interface."""
    interface_stats = psutil.net_if_stats()
    interface_addresses = psutil.net_if_addrs()

    return [
        NetworkInterface(
            name=name,
            is_up=interface_stats[name].isup,
            speed_mbps=interface_stats[name].speed,
            mtu=interface_stats[name].mtu,
            addresses=[
                NetworkAddress(
                    family=int(address.family),
                    address=address.address,
                    netmask=address.netmask,
                    broadcast=address.broadcast,
                    point_to_point=address.ptp,
                )
                for address in interface_addresses.get(name, [])
            ],
        )
        for name in sorted(interface_stats)
    ]
