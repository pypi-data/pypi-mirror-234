"""
`gh_parser`
=======================================================================
Parser to pull job contexts from .github-ci.yml files
* Author(s): Zhi Xuen Lai
"""
import logging
import re
from embedops_cli.yaml_tools import open_yaml
from ..eo_types import (
    BadYamlFileException,
    LocalRunContext,
)

_logger = logging.getLogger(__name__)


def _check_job_name(string):
    """
    Check if the job name starts with a letter or _ and
    contains only alphanumeric characters, -, or _.
    """
    # Check if the job name starts with a letter or _
    is_first_char_valid = bool(re.match("^[a-zA-Z_]", string[:1]))
    # Check if the job name contains only alphanumeric characters, -, or _
    is_whole_job_name_valid = bool(re.match("^[a-zA-Z0-9_-]*$", string))
    return is_first_char_valid and is_whole_job_name_valid


def get_job_name_list(ghyml_filename: str) -> list:
    """Get list of job names from the given YAML object"""

    try:
        ghyml = open_yaml(ghyml_filename)
    except BadYamlFileException as exc:
        raise BadYamlFileException() from exc

    job_name_list = []

    try:
        for item in ghyml["jobs"]:
            if not _check_job_name(item):
                raise BadYamlFileException()
            job_name_list.append(item)

        return job_name_list
    except (KeyError) as err:
        raise BadYamlFileException() from err


def get_job_list(glyml_filename: str) -> list:
    """Return the list of LocalRunContexts found in the given yaml object"""

    try:
        glyml = open_yaml(glyml_filename)
    except BadYamlFileException as exc:
        raise BadYamlFileException() from exc

    job_list = []

    try:
        default_var_dict = {}
        for tag, value in glyml.items():
            _logger.debug(f"tag, value: {tag}, {value}")
            # update default_var_dict
            if tag == "env":
                default_var_dict.update(value)

            if tag == "jobs":
                for job, context in value.items():
                    if not _check_job_name(job):
                        raise BadYamlFileException()
                    job_ctx = _parse_job_context(job, context, default_var_dict)

                    job_list.append(job_ctx)

        return job_list
    except (TypeError, KeyError) as err:
        raise BadYamlFileException() from err


def get_job(filename: str, job_name: str) -> LocalRunContext:
    """get a single job context object parsed from
    the pipeline yaml file"""

    try:
        ghyml = open_yaml(filename)
    except BadYamlFileException as exc:
        raise BadYamlFileException() from exc

    if not _check_job_name(job_name):
        raise BadYamlFileException()

    return _parse_job_context(job_name, ghyml["jobs"].get(job_name), {})


def _parse_job_context(yaml_tag, yaml_value, default_var_dict):  # pylint: disable=R0912
    """Return a LocalRunContexts by parsing a job context"""
    image = ""

    for step in yaml_value["steps"]:
        if step.get("uses") and step.get("uses").startswith("docker://"):
            image = step.get("uses")

    # Does not necessarily have variables
    # if it does, add them (via update()) to the default_var_dict
    var_dict = {}
    var_dict.update(default_var_dict)
    if yaml_value.get("env"):
        var_dict.update(yaml_value["env"])

    script_list = []
    if yaml_value.get("steps"):
        for line in yaml_value["steps"]:
            if line.get("with"):
                if line["with"].get("args"):
                    script_list.append(line["with"].get("args"))
                elif "github-bootstrap" not in line.get("uses"):
                    # if this is a step like actions/checkout@v3
                    # or artifact collection it's ok because
                    # other steps in job can have 'uses' clause
                    # without 'args' e.g. uses.path
                    pass
                else:
                    raise BadYamlFileException()
            elif line.get("uses") and "github-bootstrap" in line.get("uses"):
                # steps using github-bootstrap must contain with and with.args stanzas
                raise BadYamlFileException()
            if line.get("env"):
                var_dict.update(line["env"])
                keys_to_ignore = []
                pattern = r"\$\{\{(\s?)(.*?)(\s?)\}\}"
                for key, value in var_dict.items():
                    match = re.match(
                        pattern, str(value) if isinstance(value, int) else value
                    )  # force all values to str
                    if match:
                        _logger.debug(
                            f"ignoring github-style context variable '{key}' for job '{yaml_tag}'"
                        )
                        keys_to_ignore.append(key)
                for key in keys_to_ignore:
                    var_dict.pop(key, None)
    else:
        raise BadYamlFileException()

    return LocalRunContext(yaml_tag, image, script_list, var_dict)
