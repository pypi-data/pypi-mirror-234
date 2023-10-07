"""
`eo_types`
=======================================================================
Module will hold the enum classes for EmbedOps Tools
* Author(s): Bailey Steinfadt
"""

from enum import Enum
from os import getcwd
from termcolor import colored

GH_CI_CONFIG_FILENAME = ".github/workflows/embedops.yml"
BB_CI_CONFIG_FILENAME = "bitbucket-pipelines.yml"
GL_CI_CONFIG_FILENAME = ".gitlab-ci.yml"
AD_CI_CONFIG_FILENAME = "azure-pipelines.yml"
EO_CI_CONFIG_FILENAME = ".embedops-ci.yml"
SUPPORTED_CI_FILENAMES = [
    BB_CI_CONFIG_FILENAME,
    GL_CI_CONFIG_FILENAME,
    EO_CI_CONFIG_FILENAME,
    AD_CI_CONFIG_FILENAME,
    GH_CI_CONFIG_FILENAME,
]


class YamlType(Enum):
    """Types of Yaml Files EmbedOps Tools supports"""

    UNSUPPORTED = 0
    GITLAB = 1
    BITBUCKET = 2
    GITHUB = 3


class LocalRunContext:
    """Object to store the context for locally run CI jobs"""

    def __init__(
        self,
        job_name: str,
        docker_tag: str,
        script_lines: list = None,
        variables: dict = None,
    ):
        self._job_name = job_name.strip('"')
        self._docker_tag = docker_tag.strip('"')
        if script_lines is None:
            self._script = []
        else:
            self._script = script_lines
        if variables is None:
            self._variables = {}
        else:
            self._variables = variables

    def __repr__(self) -> str:
        return f"""{self.docker_tag}/{self.job_name}"""

    def __str__(self) -> str:
        return self.pretty(use_color=False)

    def pretty(self, use_color=True) -> str:
        """provide the formatted version of the parsed job
        for the end-user

        Args:
            use_color (bool, optional): color-encode the return value. Defaults to True.

        Returns:
            str: the formatted string
        """
        name = colored(self.job_name, "magenta") if use_color else self.job_name
        details = "\n".join(
            [
                f"  Image: {self.docker_tag}",
                "  Variables:",
            ]
            + [f"    - {v}" for v in self.variables]
            + [
                "  Script:",
            ]
            + [f"    - {v}" for v in self.script]
        )
        return f"{name}\n" + colored(details, "white") if use_color else details

    @property
    def job_name(self):
        """String with the name of the job"""
        return self._job_name

    @property
    def docker_tag(self):
        """String for the Docker tag the job will be launched in"""
        return self._docker_tag

    @docker_tag.setter
    def docker_tag(self, docker_tag):
        self._docker_tag = docker_tag

    @property
    def script(self):
        """List containing the job's script from the YAML file, if it exists"""
        return self._script

    @property
    def variables(self):
        """Dictionary with any variables defined in the YAML file"""
        return self._variables


##################################################################################################
########################################### EXCEPTIONS ###########################################
##################################################################################################


class EmbedOpsException(Exception):
    """Base class for all EmbedOps exceptions"""

    def __init__(
        self, message="EmbedOps encountered an internal error", fix_message=""
    ):
        self.message = message
        self.fix_message = fix_message
        super().__init__(self.message)


############################################## YAML ##############################################


class UnsupportedYamlTypeException(EmbedOpsException):
    """Raised when an Unsupported YAML type is input"""

    ERROR_MSG = "CI configuration YAML file is not one of the supported filenames\n"
    ERROR_FIX = (
        "Make sure one of the following CI configuration files is in the current directory:\n"
        "    " + "\n    ".join(SUPPORTED_CI_FILENAMES) + "\n"
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class NoYamlFileException(EmbedOpsException):
    """Raised when no YAML file is found"""

    ERROR_MSG = f"CI configuration YAML file could not be found in {getcwd()}\n"
    ERROR_FIX = (
        "Either specify a filename with the --filename option or make sure\n"
        "one of the following CI configuration files is in the current directory:\n"
        "    " + "\n    ".join(SUPPORTED_CI_FILENAMES) + "\n"
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class BadYamlFileException(EmbedOpsException):
    """Raised when a bad YAML file is found"""

    ERROR_MSG = "CI configuration YAML file could not be parsed\n"
    ERROR_FIX = (
        "Check your YAML for syntax errors. \n"
        "Email support@embedops.io if you have questions."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class MultipleYamlFilesException(EmbedOpsException):
    """Raised when multiple YAML files are found"""

    ERROR_MSG = "Multiple CI configuration files were found.\n"
    ERROR_FIX = (
        "Please specify the desired CI configuration file by using the --filename flag.\n\n"
        "Syntax: embedops-cli jobs --filename <PATH_TO_CI_CONFIG_FILE> run <JOB_NAME>"
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


######################################### Authorization ##########################################


class UnauthorizedUserException(EmbedOpsException):
    """Raised when there is no Authorization Token found in the user's secrets file"""

    ERROR_MSG = "No EmbedOps credentials found\n"

    ERROR_FIX = (
        "EmbedOps CLI is even better with an account!\n"
        "If you do not have an account and would like to learn more about EmbedOps, "
        "contact support@embedops.io"
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class LoginFailureException(EmbedOpsException):
    """Raised when logging into the Embedops backend fails"""

    ERROR_MSG = "A problem was encountered while logging into EmbedOps.\n"

    ERROR_FIX = (
        "Check your credentials on app.embedops.io and try again.\n"
        "If you encounter further issues, please contact support:\n"
        "support@embedops.io"
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


############################################# Docker #############################################


class NoDockerCLIException(EmbedOpsException):
    """Raised when docker command is not available"""

    ERROR_MSG = "docker command not found\n"
    ERROR_FIX = (
        "EmbedOps CLI requires a Docker installation.\n"
        "Head to https://docs.docker.com/get-docker and follow the instructions to install Docker."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class NoDockerContainerException(EmbedOpsException):
    """Raised when no Docker container is found in the CI configuration file"""

    ERROR_MSG = (
        "Docker container is not found in the job or in the CI configuration file.\n"
    )
    ERROR_FIX = (
        "A Docker container must be provided to run a job.\n\n"
        "For GitLab CI, use the `image` keyword.\n"
        "It can be used as part of a job, in the `default` section, or globally.\n\n"
        "For GitHub CI, use the `uses` keyword and point to the appropriate bootstrap image.\n"
        "It can only be used as part of a job."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class InvalidDockerContainerException(EmbedOpsException):
    """Raised when an invalid Docker container is detected"""

    ERROR_MSG = "Docker container is invalid.\n"
    ERROR_FIX = (
        "If your Docker container is hosted on a private registry,\n"
        "do not include http:// in your Docker container link."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class DockerNotRunningException(EmbedOpsException):
    """Raised when the Docker daemon is not running"""

    ERROR_MSG = "Docker is not running\n"
    ERROR_FIX = (
        "Start or restart Docker desktop. \n"
        "Look for the whale logo in your system status tray\n"
        'and check that it says "Docker Desktop running"'
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class DockerRegistryException(EmbedOpsException):
    """Raised when a problem accessing the registry is encountered"""

    ERROR_MSG = (
        "We were unable to authenticate with the package registry, "
        "or the image name is not correct.\n"
    )
    ERROR_FIX = (
        "To access the required Docker images needed run this job,\n"
        "login to the EmbedOps Docker registry using this command:\n"
        "\n"
        "    docker login registry.embedops.com\n"
        "\n"
        "When prompted, login with your access token, found on app.embedops.io\n"
        "Check in registry that the image name exists."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class DockerImageForBootstrapNotFound(EmbedOpsException):
    """Raised when an image is not specfied for a job that uses a bootstrap image"""

    ERROR_MSG = (
        "EMBEDOPS_IMAGE variable not specified for job that uses a bootstrap image\n"
    )
    ERROR_FIX = "Set EMBEDOPS_IMAGE: <image>:<version> in the job's YAML section\n"

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class UnknownDockerException(EmbedOpsException):
    """Raised when an error with Docker is encountered that we haven't otherwise handled"""

    ERROR_MSG = "It appears that Docker is unavailable or\nsome other error with Docker has occurred. \n"  # pylint: disable=C0301
    ERROR_FIX = (
        "1) Verify Docker is running on your machine and try again.\n"
        "2) If Docker was already running, restart Docker and try again.\n"
        "3) Then, if it's still broken, please reach out to the support team at Dojo Five:\n\n"
        "\tsupport@embedops.io\n"
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class SshDirDoesNotExistException(EmbedOpsException):
    """Raised when the directory specified in EMBEDOPS_SSH_DIR does not exist"""

    ERROR_MSG = "EMBEDOPS_SSH_DIR directory does not exist.\n"
    ERROR_FIX = "Set the correct path for EMBEDOPS_SSH_DIR in your host environment."

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class SshDirIsNotADirectoryException(EmbedOpsException):
    """Raised when the path specified in EMBEDOPS_SSH_DIR is not a directory"""

    ERROR_MSG = "EMBEDOPS_SSH_DIR path is not a directory.\n"
    ERROR_FIX = "Set the correct path for EMBEDOPS_SSH_DIR in your host environment."

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


######################################### General Errors #########################################


class NoRepoIdException(EmbedOpsException):
    """Raised when the repo id could not be found"""

    ERROR_MSG = "repo id not found\n"
    ERROR_FIX = (
        "This command requires a valid repo ID file in the project root.\n"
        "Reconnect your repository or change directories to a valid EmbedOps project."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class NoCIRunIdException(EmbedOpsException):
    """Raised when the ci run id not provided"""

    ERROR_MSG = "ci run id not found\n"
    ERROR_FIX = (
        "CI Pipeline HIL runs require a valid CIRun ID provided.\n"
        "Verify your EMBEDOPS_HOST and other platform communication\n"
        "settings are correct in your CI provider settings."
    )

    def __init__(
        self,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message, fix_message)


class NetworkException(EmbedOpsException):
    """Raised when a general network error occurs"""

    ERROR_MSG = "network exception: "
    ERROR_FIX = "Please check your network connection.\n"

    def __init__(
        self,
        status_code: int,
        message=ERROR_MSG,
        fix_message=ERROR_FIX,
    ):
        super().__init__(message + str(status_code), fix_message)
        self.status_code = status_code


class NoAvailableHilDevice(EmbedOpsException):
    """Raised when a no available HIL device is detected for CI HIL Run"""

    def __init__(self, fix_message):
        # fix_message passed in from platform
        super().__init__("HIL gateway device error", fix_message)
