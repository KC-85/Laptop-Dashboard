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


@dataclass
class MountedStorage:
    device: str
    mount_point: str
    fstype: str
    total: int
    used: int
    free: int
    percentage: float


def get_mounted_storage() -> list[MountedStorage]:
    mounted_storage: list[MountedStorage] = []

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except (PermissionError, OSError):
            continue

        mounted_storage.append(
            MountedStorage(
                device=partition.device,
                mount_point=partition.mountpoint,
                fstype=partition.fstype,
                total=usage.total,
                used=usage.used,
                free=usage.free,
                percentage=usage.percent,
            )
        )

    return mounted_storage
