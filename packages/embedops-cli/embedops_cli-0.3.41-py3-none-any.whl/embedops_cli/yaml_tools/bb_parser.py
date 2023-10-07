"""
`bb_parser`
=======================================================================
Parser to pull job contexts from bitbucket-pipelines.yml files
* Author(s): Bailey Steinfadt
"""
import logging
from embedops_cli.yaml_tools import open_yaml
from ..eo_types import BadYamlFileException, LocalRunContext

_logger = logging.getLogger(__name__)


def get_job_name_list(bbyml_filename: str):
    """Get list of job names from the given YAML object"""

    try:
        bbyml = open_yaml(bbyml_filename)
    except BadYamlFileException as exc:
        raise BadYamlFileException() from exc

    job_name_list = []

    try:
        for job_def in bbyml["pipelines"]["default"]:
            if "step" in job_def:
                job_name_list.append(job_def["step"]["name"])

            elif "parallel" in job_def:
                for par_step in job_def["parallel"]:
                    job_name_list.append(par_step["step"]["name"])

        if not all(isinstance(job_name, str) for job_name in job_name_list):
            raise BadYamlFileException()

        return job_name_list
    except (KeyError) as err:
        raise BadYamlFileException() from err


def get_job_list(bbyml_filename: str) -> list:
    """Return the list of LocalRunContexts found in the given yaml object"""

    try:
        bbyml = open_yaml(bbyml_filename)
    except BadYamlFileException as exc:
        raise BadYamlFileException() from exc

    job_names = get_job_name_list(bbyml_filename)

    try:
        job_list = []
        for job_name in job_names:
            job_list.append(get_job(bbyml_filename, job_name, bbyml))

        return job_list
    except (KeyError, AttributeError, TypeError) as err:
        raise BadYamlFileException() from err


def get_job(filename: str, job_name: str, bbyml: dict = None) -> LocalRunContext:
    """get a single job context object parsed from
    the pipeline yaml file"""
    default_image = "atlassian/default-image:latest"
    job = None
    if not bbyml:
        try:
            bbyml = open_yaml(filename)
        except BadYamlFileException as exc:
            raise BadYamlFileException() from exc

    for job_def in bbyml["pipelines"].get("default", {}):
        if "step" in job_def:
            if job_name == job_def["step"]["name"]:
                job = _parse_job_context(job_def, default_image)
        elif "parallel" in job_def:
            for par_step in job_def["parallel"]:
                if "step" in par_step:
                    print(f"par_step: {par_step}")
                    if job_name == par_step["step"]["name"]:
                        job = _parse_job_context(par_step, default_image, parallel=True)

    return job


def _parse_job_context(yaml_value, default_image, parallel=False):
    # TODO: parse for other pipelines (branches, tags, pull-requests, custom)
    # TODO: parse for definitions and YAML anchors

    script_list = []

    if "script" in yaml_value["step"]:
        for line in yaml_value["step"]["script"]:
            script_list.append(line)
    image = ""
    if "image" in yaml_value["step"]:
        image = yaml_value["step"]["image"]["name"]
    else:
        # NOTE: due to the ParallelNoImage assertion
        # in bb_parser_test.py::test_get_job_list,
        # only non-parallel jobs will get a default image
        image = default_image if not parallel else ""
    return LocalRunContext(yaml_value["step"]["name"], image, script_list)
