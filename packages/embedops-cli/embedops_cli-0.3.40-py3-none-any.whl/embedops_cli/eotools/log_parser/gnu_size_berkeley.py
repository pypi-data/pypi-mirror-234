"""Regex pattern for parsing the output of `size` in the berkeley format"""
# regex pattern for arm-gcc-eabi-size in Berkeley format
# Example:
# https://regex101.com/r/f0wctA/1
# [ 99%] Linking C executable application.elf
#   text	   data	    bss	    dec	    hex	filename
#  130584	   2064	  69440	 202088	  31568	application.elf

# bss=>RAM
# data=>RAM (variables) + FLASH (initialization constants)
# text=> FLASH
SIZE_PATTERN = (
    r"text\s+data\s+bss\s+dec\s+hex\s+filename\n\s*"
    r"(?P<flash_code_size>\d+)\s+"
    r"(?P<flash_data_size>\d+)\s+"
    r"(?P<ram_size>\d+)\s+"
    r"(?P<dec>\d+)\s+"
    r"(?P<hex>[a-fA-F0-9]+)\s+"
    r"(?P<target_name>\S+)"
)


def pack_result(result: dict) -> dict:
    """Helper function to pack results from regex
    matching of berkely size pattern from GCC/TI log files.

    Args:
        result (dict): a group_dict() from a regex match

    Returns:
        dict: memory metrics for reporting to platform
    """
    storage_sizes = {
        "flash_code_size": None,
        "flash_data_size": None,
        "ram_size": None,
    }
    storage_sizes["ram_size"] = int(result["ram_size"].replace("'", ""))
    storage_sizes["flash_code_size"] = int(result["flash_code_size"].replace("'", ""))
    storage_sizes["flash_data_size"] = int(result["flash_data_size"].replace("'", ""))
    storage_sizes["flash_data_size"] += int(result["ram_size"])
    storage_sizes["dimensions"] = {
        "build_target_name": result["target_name"],
    }
    if "target_group" in result.groupdict():
        storage_sizes["dimensions"]["build_target_group"] = result["target_group"]
    # TODO: deprecate this dimension re:eo-548
    if storage_sizes["dimensions"].get("build_target_group"):
        storage_sizes["dimensions"]["build_target"] = " - ".join(
            [
                storage_sizes["dimensions"]["build_target_name"],
                storage_sizes["dimensions"]["build_target_group"],
            ]
        )
    else:
        storage_sizes["dimensions"]["build_target"] = storage_sizes["dimensions"][
            "build_target_name"
        ]
    return storage_sizes
