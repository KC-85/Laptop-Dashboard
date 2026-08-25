"""Unit tests for network traffic and interface statistics."""

from socket import AF_INET, AF_INET6
from types import SimpleNamespace
from unittest.mock import patch

from sysoverview.network import stats


def test_get_network_totals() -> None:
    counters = SimpleNamespace(
        bytes_sent=1_000,
        bytes_recv=2_000,
        packets_sent=10,
        packets_recv=20,
        errin=1,
        errout=2,
        dropin=3,
        dropout=4,
    )

    with patch.object(
        stats.psutil,
        "net_io_counters",
        return_value=counters,
    ) as mock_net_io_counters:
        result = stats.get_network_totals()

    mock_net_io_counters.assert_called_once_with()
    assert result == stats.NetworkTotals(
        bytes_sent=1_000,
        bytes_received=2_000,
        packets_sent=10,
        packets_received=20,
        errors_in=1,
        errors_out=2,
        dropped_in=3,
        dropped_out=4,
    )


def test_get_network_interfaces() -> None:
    interface_stats = {
        "wlan0": SimpleNamespace(isup=True, speed=866, mtu=1500),
        "eth0": SimpleNamespace(isup=False, speed=1_000, mtu=1500),
    }
    interface_addresses = {
        "wlan0": [
            SimpleNamespace(
                family=AF_INET,
                address="192.168.1.25",
                netmask="255.255.255.0",
                broadcast="192.168.1.255",
                ptp=None,
            )
        ],
        "eth0": [
            SimpleNamespace(
                family=AF_INET6,
                address="fe80::1%eth0",
                netmask="ffff:ffff:ffff:ffff::",
                broadcast=None,
                ptp=None,
            )
        ],
    }

    with (
        patch.object(stats.psutil, "net_if_stats", return_value=interface_stats),
        patch.object(stats.psutil, "net_if_addrs", return_value=interface_addresses),
    ):
        result = stats.get_network_interfaces()

    assert result == [
        stats.NetworkInterface(
            name="eth0",
            is_up=False,
            speed_mbps=1_000,
            mtu=1500,
            addresses=[
                stats.NetworkAddress(
                    family=int(AF_INET6),
                    address="fe80::1%eth0",
                    netmask="ffff:ffff:ffff:ffff::",
                    broadcast=None,
                    point_to_point=None,
                )
            ],
        ),
        stats.NetworkInterface(
            name="wlan0",
            is_up=True,
            speed_mbps=866,
            mtu=1500,
            addresses=[
                stats.NetworkAddress(
                    family=int(AF_INET),
                    address="192.168.1.25",
                    netmask="255.255.255.0",
                    broadcast="192.168.1.255",
                    point_to_point=None,
                )
            ],
        ),
    ]


def test_get_network_interface_without_addresses() -> None:
    interface_stats = {
        "eth0": SimpleNamespace(isup=False, speed=0, mtu=1500),
    }

    with (
        patch.object(stats.psutil, "net_if_stats", return_value=interface_stats),
        patch.object(stats.psutil, "net_if_addrs", return_value={}),
    ):
        result = stats.get_network_interfaces()

    assert result == [
        stats.NetworkInterface(
            name="eth0",
            is_up=False,
            speed_mbps=0,
            mtu=1500,
            addresses=[],
        )
    ]
