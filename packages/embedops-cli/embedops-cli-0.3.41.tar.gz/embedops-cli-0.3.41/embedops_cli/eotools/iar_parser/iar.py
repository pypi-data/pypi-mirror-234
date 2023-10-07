"""Regex pattern for parsing IAR map file, exceptions, and helper functions"""
from embedops_cli.eo_types import EmbedOpsException


COMPILER_PATTERN = r"IAR ANSI C/C++ Compiler (V8.50.1.245/W32) for ARM"

# regex pattern for IAR size default output
# Example:
# https://regex101.com/r/5g5Yon/1
#
#      337'642 bytes of readonly  code memory
#   31'974'173 bytes of readonly  data memory
#    7'394'959 bytes of readwrite data memory
#
# Errors: none
# Warnings: none


SIZE_PATTERN = (
    r"\s+(?P<flash_code_size>[\d']+).+readonly\s+code.+\n"
    r"\s+(?P<flash_data_size>[\d']+).+readonly\s+data.+\n"
    r"\s+(?P<ram_size>[\d']+).+readwrite\s+data.+\n"
)

WARNING_PATTERN = (
    r"(?:\"?(.*?)\"?[\(,](\d+)\)?\s+(?::\s)?)"
    r"(Error|Remark|Warning|Fatal[E|e]rror)\[(.*)\]: (.*)$"
)


def pack_result(result: dict, mapfile_name: str, iar_config: str) -> dict:
    """Helper function to pack results from regex
    matching of size pattern from an IAR map file.

    Args:
        result (dict): a group_dict() from a regex match

    Returns:
        dict: memory metrics for reporting to platform
    """
    result["flash_code_size"] = int(result["flash_code_size"].replace("'", ""))
    result["flash_data_size"] = int(result["flash_data_size"].replace("'", ""))
    result["ram_size"] = int(result["ram_size"].replace("'", ""))
    result["dimensions"] = {
        "build_target": " - ".join([mapfile_name, iar_config]),
    }
    result["dimensions"].update(
        {"build_target_name": mapfile_name, "build_target_group": iar_config}
    )
    return result


class IARNoMemoryMetricsFoundInMapFileException(EmbedOpsException):
    """Exception for unable to find memory metrics in .map file."""

    pass  # pylint: disable=W0107
