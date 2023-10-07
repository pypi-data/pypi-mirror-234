"""Utilities for parsing and manipulating image files"""

import logging
import fs


# Static values from MBR specification
MBR_SIZE_BYTES = 512  # Size of the entire MBR table size
SECTOR_SIZE_BYTES = 512
PARTITION_ENTRY_SIZE = 16
BOOT_PARTITION_ENTRY_OFFSET = 446
PARTITION_STATUS_OK = 0x80
PARTITION_TYPE_FAT32 = 0x0C

_logger = logging.getLogger(__name__)


def write_image_config(image_path: str, config_string: str) -> bool:

    """Write the given config string to config.json,
    a file on the boot partition of the given image"""

    # First, open the image and grab data from the MBR
    with open(image_path, "rb") as image_file:
        mbr_data = image_file.read(MBR_SIZE_BYTES)

    if len(mbr_data) != MBR_SIZE_BYTES:
        return False

    partition_zero_data = mbr_data[
        BOOT_PARTITION_ENTRY_OFFSET : BOOT_PARTITION_ENTRY_OFFSET + PARTITION_ENTRY_SIZE
    ]

    # These offsets come from the MBR specification
    boot_partition_status = partition_zero_data[0x00]
    boot_partition_type = partition_zero_data[0x04]
    boot_partition_offset = int.from_bytes(
        partition_zero_data[0x08:0x0C], byteorder="little"
    )

    if (
        boot_partition_status != PARTITION_STATUS_OK
        or boot_partition_type != PARTITION_TYPE_FAT32
    ):
        return False

    boot_partition_offset *= SECTOR_SIZE_BYTES

    boot_fs = fs.open_fs(f"fat://{image_path}?offset={boot_partition_offset}")
    config_file = boot_fs.open("config.json", "w")
    config_file.write(config_string)

    config_file.close()
    boot_fs.close()

    return True
