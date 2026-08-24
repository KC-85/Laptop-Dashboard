"""
Collect storage usage statistics for the root filesystem.

Storage statistics include total, used, and free space in bytes,
along with the usage percentage. Human-readable formatting is
handled by the presentation layer.
"""


from dataclasses import dataclass

import psutil


@dataclass
class StorageStats:
    total: int
    used: int
    free: int
    percentage: float


def get_storage_stats() -> StorageStats:
    usage = psutil.disk_usage("/")

    return StorageStats(
        total=usage.total,
        used=usage.used,
        free=usage.free,
        percentage=usage.percent,
    )


def get_filesystem_type() -> str | None:
    filesystem = psutil.disk_partitions()
    for partition in filesystem:
        if partition.mountpoint == "/":
            return partition.fstype
    return None
