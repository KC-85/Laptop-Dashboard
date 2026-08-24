"""Unit tests for root filesystem storage statistics."""

from types import SimpleNamespace
from unittest.mock import patch

from laptop_dashboard.storage import stats


def test_get_storage_stats() -> None:
    mock_usage = SimpleNamespace(
        total=256 * 1024**3,
        used=128 * 1024**3,
        free=128 * 1024**3,
        percent=50.0,
    )

    with patch.object(stats.psutil, "disk_usage", return_value=mock_usage) as mock_disk_usage:
        storage = stats.get_storage_stats()

    mock_disk_usage.assert_called_once_with("/")
    assert storage == stats.StorageStats(
        total=256 * 1024**3,
        used=128 * 1024**3,
        free=128 * 1024**3,
        percentage=50.0,
    )


def test_get_filesystem_type() -> None:
    partitions = [
        SimpleNamespace(mountpoint="/boot", fstype="vfat"),
        SimpleNamespace(mountpoint="/", fstype="ext4"),
    ]

    with patch.object(stats.psutil, "disk_partitions", return_value=partitions):
        assert stats.get_filesystem_type() == "ext4"


def test_get_filesystem_type_when_root_is_missing() -> None:
    partitions = [SimpleNamespace(mountpoint="/boot", fstype="vfat")]

    with patch.object(stats.psutil, "disk_partitions", return_value=partitions):
        assert stats.get_filesystem_type() is None


def test_get_mounted_storage() -> None:
    partitions = [
        SimpleNamespace(device="/dev/sda1", mountpoint="/", fstype="ext4"),
        SimpleNamespace(device="/dev/sda2", mountpoint="/boot", fstype="vfat"),
    ]

    mock_usage_root = SimpleNamespace(
        total=256 * 1024**3,
        used=128 * 1024**3,
        free=128 * 1024**3,
        percent=50.0,
    )

    mock_usage_boot = SimpleNamespace(
        total=512 * 1024**2,
        used=256 * 1024**2,
        free=256 * 1024**2,
        percent=50.0,
    )

    with (
        patch.object(stats.psutil, "disk_partitions", return_value=partitions),
        patch.object(
            stats.psutil,
            "disk_usage",
            side_effect=[mock_usage_root, mock_usage_boot],
        ),
    ):
        mounted_storage = stats.get_mounted_storage()

    assert len(mounted_storage) == 2
    assert mounted_storage[0] == stats.MountedStorage(
        device="/dev/sda1",
        mount_point="/",
        fstype="ext4",
        total=256 * 1024**3,
        used=128 * 1024**3,
        free=128 * 1024**3,
        percentage=50.0,
    )
    assert mounted_storage[1] == stats.MountedStorage(
        device="/dev/sda2",
        mount_point="/boot",
        fstype="vfat",
        total=512 * 1024**2,
        used=256 * 1024**2,
        free=256 * 1024**2,
        percentage=50.0,
    )
