"""Methods for parsing IAR project (.ewp) files."""
import os
from bs4.element import ResultSet
from bs4 import BeautifulSoup as bs
from embedops_cli.utilities import logging_setup
from embedops_cli.eo_types import EmbedOpsException


_logger = logging_setup(__name__)


def get_all_project_configurations(iar_ewp_file: str) -> ResultSet:
    """Get a list of all project configurations from
    an IAR project (.ewp) file

    Args:
        iar_ewp_file (str): filesystem path to the IAR project (.ewp) file

    Raises:
        IAREwpFileNotFoundException: IAR project file not found.

    Returns:
        ResultSet: A bs4 object containing the requested XML elements.
    """
    resultset = ResultSet
    if not os.path.exists(iar_ewp_file):
        raise IAREwpFileNotFoundException(
            message=f"IAR project file not found: {iar_ewp_file}"
        )

    with open(iar_ewp_file, "rb") as ewp_file:
        try:
            bs_ewp_file = bs(ewp_file, "xml")
            resultset = bs_ewp_file.find_all("configuration")
        except (OSError, IOError) as err:
            print(f"OS/IO ERROR: {err}")
    return resultset


def get_project_configuration_settings(
    configurations: ResultSet, iar_build_config: str
) -> ResultSet:
    """Searches an IAR project file for a specific configuration's
    <settings> object.

    Args:
        configurations (ResultSet): Set of all configurations in the .ewp file.
        iar_build_config (str): The build configuration (e.g. Debug, Production, etc.)

    Raises:
        IARProjectSettingsNotFoundException: <settings> not found in requested configuration.

    Returns:
        ResultSet: A bs4 object containing the requested XML elements.
    """
    proj_settings = ResultSet
    for proj_conf in configurations:
        proj_conf_name = proj_conf.find("name").text
        _logger.debug(
            f"searching for iar config: {iar_build_config} == {proj_conf_name}"
        )
        if proj_conf_name == iar_build_config:
            proj_settings = proj_conf.find_all("settings")
            break
    else:
        raise IARProjectSettingsNotFoundException(
            message=f"Unable to find project settings for '{iar_build_config}' in {configurations}"
        )
    return proj_settings


def get_configuration_general_data(project_settings: ResultSet) -> ResultSet:
    """Searches all project settings for the "General" settings
    and returns the object containing the <data> element.

    Args:
        project_settings (ResultSet): A bs4 object containing all <settings> in the .ewp file.

    Returns:
        ResultSet: A bs4 object containing the requested XML elements.
    """
    general_data = ResultSet

    for proj_setting in project_settings:
        proj_setting_name = proj_setting.find("name").text
        _logger.debug(f"searching for project setting: General == {proj_setting_name}")
        if proj_setting_name == "General":
            general_data = proj_setting.find("data")
            break
    return general_data


def get_configuration_ilink_data(project_settings: ResultSet) -> ResultSet:
    """Searches all project settings for the "ILINK" settings
    and returns the object containing the <data> element.

    Args:
        project_settings (ResultSet): A bs4 object containing all <settings> in the .ewp file.

    Returns:
        ResultSet: A bs4 object containing the requested XML elements.
    """
    general_data = ResultSet
    for proj_setting in project_settings:
        proj_setting_name = proj_setting.find("name").text
        _logger.debug(f"searching for project setting: ILINK == {proj_setting_name}")
        if proj_setting_name == "ILINK":
            general_data = proj_setting.find("data")
            break
    return general_data


def get_configuration_list_path(iar_ewp_file: str, iar_build_config: str) -> str:
    """Searches the "General" data object for the "ListPath" value, which
    is the relative path from the IAR project file to where the compiler
    outputs are places (e.g. .out, .hex, .map, etc.).

    Args:
        iar_ewp_file (str): Filesystem path to the IAR project (.ewp) file.
        iar_build_config (str): The build configuration (e.g. Debug, Production, etc.)

    Raises:
        IARNoListOptionException: IAR project file does not contain ListPath setting.

    Returns:
        str: The relative path to the configuration's build output directory.
    """
    list_path = None

    configs = get_all_project_configurations(iar_ewp_file)
    proj_settings = get_project_configuration_settings(configs, iar_build_config)
    general_data = get_configuration_general_data(proj_settings)

    for option in general_data.find_all("option"):
        option_name = option.find("name").text
        _logger.debug(f"searching for setting option: ListPath == {option_name}")
        if option_name == "ListPath":
            list_path = option.find("state").text
            _logger.debug(f"found ListPath: {list_path}")
            break

    if not list_path:
        raise IARNoListOptionException(
            message=f"ListPath option in '{iar_ewp_file}' for config '{iar_build_config}' not found."  # pylint: disable=C0301
        )

    return list_path


def get_configuration_ilinkoutputfile(iar_ewp_file: str, iar_build_config: str) -> str:
    """The the name of the output (.out) file for the given IAR configuration.

    Args:
        iar_ewp_file (str): Filesystem path to the IAR project (.ewp) file.
        iar_build_config (str): The build configuration (e.g. Debug, Production, etc.)

    Raises:
        IARNoIlinkOutputFileOptionException: Could not find the IlinkOutputFile (e.g. MyBinary.out)

    Returns:
        str: The name of the .out file as specified in the IAR configuration.
    """
    outfile = None

    configs = get_all_project_configurations(iar_ewp_file)
    proj_settings = get_project_configuration_settings(configs, iar_build_config)
    # _logger.debug(f'looking for ilink data with project settings: {proj_settings}')
    ilink_data = get_configuration_ilink_data(proj_settings)

    for option in ilink_data.find_all("option"):
        option_name = option.find("name").text
        _logger.debug(f"searching for setting option: IlinkOutputFile == {option_name}")
        if option_name == "IlinkOutputFile":
            outfile = option.find("state").text
            _logger.debug(f"found IlinkOutputFile: {outfile}")
            break

    if not outfile:
        raise IARNoIlinkOutputFileOptionException(
            message=f"IlinkOutputFile option in '{iar_ewp_file}' for config '{iar_build_config}' not found."  # pylint: disable=C0301
        )

    return outfile


def get_configuration_mapfile_path(ewp_path: str, iar_config: str) -> str:
    """Create the filesystem path to the .map file from the specified
    IAR configuration.

    Args:
        iar_ewp_file (str): Filesystem path to the IAR project (.ewp) file.
        iar_build_config (str): The build configuration (e.g. Debug, Production, etc.)

    Raises:
        IAREwpFileNotFoundException: The IAR project file given does not exist.

    Returns:
        str: The filesystem path to the .map file for the given IAR configuration.
    """
    if not os.path.exists(ewp_path):
        raise IAREwpFileNotFoundException(
            message=f"IAR project file does not exist: {ewp_path}"
        )
    ewp_file = os.path.basename(ewp_path)
    ewp_dir = os.path.dirname(ewp_path)
    mapfile_name_raw = get_configuration_ilinkoutputfile(ewp_path, iar_config).strip(
        ".out"
    )
    if mapfile_name_raw.startswith("$") and mapfile_name_raw.endswith("$"):
        val = mapfile_name_raw.strip("$")
        if val == "PROJ_FNAME":
            mapfile_name = ewp_file.replace(".ewp", "")

    else:
        mapfile_name = ewp_file.replace(".ewp", "")
    list_path_raw = get_configuration_list_path(ewp_path, iar_config)
    list_path = list_path_raw.replace("\\", "/")  # windows-style paths
    mapfile_path = os.path.join(
        os.path.abspath(ewp_dir), list_path, mapfile_name + ".map"
    )
    if not os.path.exists(mapfile_path):
        raise IARMapFileNotFoundException(
            message=f"Mapfile not found at path: {mapfile_path}"
        )
    return mapfile_path


class IARMapFileNotFoundException(EmbedOpsException):
    """Exception for unable to find ListPath in .ewp file."""

    pass  # pylint: disable=W0107


class IARNoListOptionException(EmbedOpsException):
    """Exception for unable to find ListPath in .ewp file."""

    pass  # pylint: disable=W0107


class IARNoIlinkOutputFileOptionException(EmbedOpsException):
    """Exception for unable to find IlinkOutputFile in .ewp file."""

    pass  # pylint: disable=W0107


class IARProjectSettingsNotFoundException(EmbedOpsException):
    """Exception for unable to find certain settings in .ewp file."""

    pass  # pylint: disable=W0107


class IAREwpFileNotFoundException(EmbedOpsException):
    """Exception for unable to find .ewp file."""

    pass  # pylint: disable=W0107
