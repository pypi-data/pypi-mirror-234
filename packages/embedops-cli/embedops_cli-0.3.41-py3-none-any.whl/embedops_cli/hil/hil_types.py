"""Common types and constants used by the HIL commands"""
import os
from embedops_cli.eo_types import EmbedOpsException


def get_hil_config_path():
    """Return the path to the HIL config YAML file"""
    return os.path.join(
        os.path.abspath(os.path.curdir), ".embedops", "hil", "config.yml"
    )


class HILRepoId404Exception(EmbedOpsException):
    """Raised when the repo id could not be found by the platform,
    indicated by a 404 response"""

    ERROR_MSG = "repo id not found\n"
    ERROR_FIX = (
        "The server was not able to find the repo id given in the file repo_id.yml.\n"
        "Make sure this ID is correct and verify a Balena fleet is associated with it."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class NoHILRootPathException(EmbedOpsException):
    """Raised when the hil_root_path attribute could not be read from
    the .embedops/hil/config.yml file"""

    ERROR_MSG = "hil root path not found\n"
    ERROR_FIX = (
        f"This command requires a HIL root path defined in {get_hil_config_path()}:hil_root_path.\n"
        "Set up the file or change directories to a valid EmbedOps project."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class HILFilesInvalidException(EmbedOpsException):
    """Raised when the hil_root_path either contains no files or
    contains syntactically invalid files"""

    ERROR_MSG = "hil files not valid\n"
    ERROR_FIX = f"This command requires valid Python code in the HIL root path.\n"

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
        additional_message="",
    ):
        super().__init__(message, fix_message + f"{additional_message}\n")


class NoHILArtifactsPathException(EmbedOpsException):
    """Raised when the hil_artifacts attribute could not be read from
    the .embedops/hil/config.yml file, or the file does not exist"""

    ERROR_MSG = "hil artifacts path not found\n"
    ERROR_FIX = (
        f"This command requires a HIL artifacts path defined in "
        f"{get_hil_config_path()}:hil_artifacts.\n"
        "Set up the file and make sure the given artifacts exist."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class HILRootPathDoesNotExistException(EmbedOpsException):
    """Raised when the hil_root_path attribute points to a path that doesn't exist."""

    ERROR_MSG = "hil root path does not exist\n"
    ERROR_FIX = (
        f"The HIL root path defined in {get_hil_config_path()} does not exist.\n"
        "Change the path or change directories to a valid EmbedOps project."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class HILPackageCreationException(EmbedOpsException):
    """Raised when the HIL execution could not be created"""

    ERROR_MSG = "hil execution package not created\n"
    ERROR_FIX = (
        "The HIL execution package could not be created.\n"
        f"Please verify the HIL config file located at {get_hil_config_path()}."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class HILImageConfigException(EmbedOpsException):
    """Raised when the gateway image could not be configured"""

    ERROR_MSG = "hil gateway image unable to be configured\n"
    ERROR_FIX = (
        "The gateway image file could not be configured.\n"
        "Please try the operation again."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)
