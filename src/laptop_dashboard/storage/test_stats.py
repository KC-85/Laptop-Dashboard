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
