"""
`ad_parser`
=======================================================================
Parser to pull job contexts from azure-pipelines.yml files
* Author(s): Jimmy Gomez
"""
import logging
import re
from embedops_cli.yaml_tools import open_yaml
from ..eo_types import BadYamlFileException, LocalRunContext

_logger = logging.getLogger(__name__)


def get_job_name_list(adyml_filename: str):
    """Get list of job names from the given YAML object"""

    try:
        adyml = open_yaml(adyml_filename)
    except BadYamlFileException as exc:
        raise BadYamlFileException() from exc

    job_name_list = []

    try:
        for job_def in adyml["jobs"]:
            if "job" in job_def:
                job_name_list.append(job_def["job"])

        if not all(isinstance(job_name, str) for job_name in job_name_list):
            raise BadYamlFileException()

        return job_name_list
    except (KeyError) as err:
        raise BadYamlFileException() from err


def get_job_list(adyml_filename: str) -> list:
    """Return the list of LocalRunContexts found in the given yaml object"""

    try:
        job_list = []
        for job_name in get_job_name_list(adyml_filename):
            job_list.append(get_job(adyml_filename, job_name))

        return job_list
    except (KeyError, AttributeError, TypeError) as err:
        raise BadYamlFileException() from err


def get_job(filename: str, job_name: str, adyml: dict = None) -> LocalRunContext:
    """get a single job context object parsed from
    the pipeline yaml file"""
    job = None
    default_image = "ubuntu:latest"
    if not adyml:
        try:
            adyml = open_yaml(filename)
        except BadYamlFileException as exc:
            raise BadYamlFileException() from exc

    for job_def in adyml["jobs"]:
        if "job" in job_def:
            if job_name == job_def["job"]:
                job = _parse_job_context(job_def, default_image)

    return job


def _parse_job_context(yaml_value, default_image):
    image = default_image
    var_dict = {}
    script_list = []
    if "steps" in yaml_value:
        for step in yaml_value["steps"]:
            if "script" in step:
                script_list += _parse_script(step)
    if "container" in yaml_value:
        if isinstance(yaml_value["container"], str):
            image = yaml_value["container"]
        elif isinstance(yaml_value["container"], dict):
            if "image" in yaml_value["container"]:
                image = yaml_value["container"]["image"]
            if "env" in yaml_value["container"]:
                var_dict.update(yaml_value["container"]["env"])
    # ignore variable syntax for using azure repo variable
    for var_name, var_value in var_dict.copy().items():
        if re.match(r"\$\(.*\)$", var_value):
            del var_dict[var_name]
    return LocalRunContext(yaml_value["job"], image, script_list, var_dict)


def _parse_script(step):
    script_list = []
    if isinstance(step["script"], list):
        for line in step["script"]:
            script_list.append(line)
    elif isinstance(step["script"], str):
        script_list += step["script"].split("\n")
        if script_list[-1] == "":
            # Remove the last empty command
            script_list.pop(-1)
    else:
        raise BadYamlFileException()
    return script_list
