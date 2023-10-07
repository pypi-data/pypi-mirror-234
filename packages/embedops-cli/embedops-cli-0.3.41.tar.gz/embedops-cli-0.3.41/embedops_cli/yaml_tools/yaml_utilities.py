"""
`yaml_utilities`
=======================================================================
Shared YAML parsing utilities
* Author(s): Bailey Steinfadt, Bryan Siepert, Jimmy Gomez
"""

from os import listdir, path
from embedops_cli.yaml_tools import bb_parser, gl_parser, gh_parser, ad_parser
from embedops_cli.docker_run import DOCKER_DOMAIN
from embedops_cli.utilities import logging_setup
from embedops_cli.eo_types import (
    BadYamlFileException,
    NoYamlFileException,
    UnsupportedYamlTypeException,
    LocalRunContext,
    SUPPORTED_CI_FILENAMES,
    GH_CI_CONFIG_FILENAME,
    GL_CI_CONFIG_FILENAME,
    BB_CI_CONFIG_FILENAME,
    AD_CI_CONFIG_FILENAME,
    EO_CI_CONFIG_FILENAME,
)

_logger = logging_setup(__name__)


def get_job_context_for_name(
    parser, yml_filename: str, requested_name: str
) -> LocalRunContext:
    """Get job context for requested job name from specified yml object"""

    try:
        for job in parser.get_job_list(yml_filename):
            if job.job_name == requested_name:
                return job
    except BadYamlFileException as exc:
        raise BadYamlFileException() from exc

    # if job was not found, return None
    return None


def get_yaml_in_directory(directory="."):
    """Looks for supported YAML files in the indicated directory"""
    current_dir_files = listdir(directory)
    for dir_file in SUPPORTED_CI_FILENAMES:
        if dir_file in current_dir_files:
            filename = dir_file

            _logger.debug(f"Found YAML: {filename} in directory: {directory}")
            break
    else:
        if path.exists(GH_CI_CONFIG_FILENAME):
            filename = GH_CI_CONFIG_FILENAME
        else:
            raise NoYamlFileException()

    return filename


def _fully_qualify_bootstrap_tag(job: LocalRunContext) -> str:
    """parses the target images from EMBEDOPS_IMAGE env var
    from those jobs that require a bootstrap"""
    # if bootstrap detected, use EMBEDOPS_IMAGE variable to specify
    # desired image. if variable not specified, set image to None
    # to trigger error after job detail output
    if job:
        if (
            "gitlab-bootstrap" in job.docker_tag
            or "azure-bootstrap" in job.docker_tag
            or "github-bootstrap" in job.docker_tag
        ):
            docker_image = job.variables.get("EMBEDOPS_IMAGE")
            job.docker_tag = (
                f"{DOCKER_DOMAIN}/" + docker_image if docker_image else docker_image
            )


def get_job_list(filename: str) -> list:
    """Retrieve the job list from the given file using the required parser"""
    try:
        parser = get_correct_parser_type(filename)
    except UnsupportedYamlTypeException as exc:
        raise UnsupportedYamlTypeException() from exc

    try:
        job_list = parser.get_job_list(filename)
        for job in job_list:
            _fully_qualify_bootstrap_tag(job)
        return job_list
    except BadYamlFileException as exc:
        raise BadYamlFileException() from exc


def get_job(filename: str, job_name: str):
    """CI Provider portable method for getting
    a single job context object parsed from
    the pipeline yaml file"""
    try:
        parser = get_correct_parser_type(filename)
        _logger.debug(f"parsing {job_name} from {filename}")
        job = parser.get_job(filename, job_name)
        _fully_qualify_bootstrap_tag(job)
        return job
    except UnsupportedYamlTypeException as exc:
        raise UnsupportedYamlTypeException() from exc


def get_correct_parser_type(filename: str):
    """Get the parser for a given filename"""
    normalized_filename = filename.lower()
    if GL_CI_CONFIG_FILENAME in normalized_filename:
        return gl_parser
    if EO_CI_CONFIG_FILENAME in normalized_filename:
        return gl_parser
    if BB_CI_CONFIG_FILENAME in normalized_filename:
        return bb_parser
    if AD_CI_CONFIG_FILENAME in normalized_filename:
        return ad_parser
    if GH_CI_CONFIG_FILENAME in normalized_filename:
        return gh_parser
    raise UnsupportedYamlTypeException()
