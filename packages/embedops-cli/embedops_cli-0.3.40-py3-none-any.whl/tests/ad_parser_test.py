"""
`gl_parser_test`
=======================================================================
Unit tests for the parser to pull job contexts from .gitlab-ci.yml files
* Author(s): Bailey Steinfadt
"""
import pytest

from embedops_cli.yaml_tools import ad_parser, yaml_utilities
from embedops_cli.eo_types import BadYamlFileException
from tests import ADYML_FILENAME

ADYML_MISSING_STEP_NAME_VALUE_FILENAME = (
    "tests/ad-pipelines/test-missing-image-name-value-azure-pipelines.yml"
)
ADYML_MISSING_SCRIPT_VALUE_FILENAME = (
    "tests/ad-pipelines/test-missing-script-value-azure-pipelines.yml"
)


def test_get_job_list_with_missing_image_name_value_exception():
    """test that exception is raised for job with missing image name value"""
    with pytest.raises(BadYamlFileException):
        assert ad_parser.get_job_list(ADYML_MISSING_STEP_NAME_VALUE_FILENAME)


def test_get_job_list_with_missing_script_value_exception():
    """test that exception is raised for job with missing script value"""
    with pytest.raises(BadYamlFileException):
        assert ad_parser.get_job_list(ADYML_MISSING_SCRIPT_VALUE_FILENAME)


def test_get_job_name_list():
    """Test retrieving the list of job names from the YAML"""
    job_name_list = ad_parser.get_job_name_list(ADYML_FILENAME)
    assert len(job_name_list) == 4
    assert job_name_list[0] == "build"
    assert job_name_list[2] == "cppcheck"


def test_get_job_list():
    """Test retrieving the list of complete local run context from the YAML"""
    job_list = ad_parser.get_job_list(ADYML_FILENAME)
    assert len(job_list) == 4
    assert job_list[0].job_name == "build"
    assert len(job_list[0].docker_tag) > 0
    assert len(job_list[0].script) > 0
    assert job_list[2].job_name == "cppcheck"
    assert len(job_list[0].docker_tag) > 0
    assert len(job_list[0].script) > 0


def test_get_job_list_default_image():
    """Test retrieving the list of complete local run context from the YAML
    where the step uses the default image"""
    job_list = ad_parser.get_job_list(ADYML_FILENAME)
    job = [job for job in job_list if job.job_name == "no-image"][0]
    assert job.job_name == "no-image"
    assert len(job.docker_tag) > 0
    assert len(job.script) > 0


def test_get_job_context():
    """Test getting the job context for an indicated job"""
    requested_name = "build"
    job = yaml_utilities.get_job_context_for_name(
        ad_parser, ADYML_FILENAME, requested_name
    )
    assert job.job_name == requested_name


def test_step_with_literal_multiline_block():
    """Test retrieving a literal multiline block"""
    job = yaml_utilities.get_job_context_for_name(ad_parser, ADYML_FILENAME, "build")
    assert (
        job.script[0]
        == 'embedops-azure-run "pip install protobuf grpcio-tools && embedops-build make debug"'
    )
    assert job.script[1] == 'echo "more"'


def test_get_job_context_ignores_azure_variables():
    """Test that variables specified with $(.*) are ignored"""
    requested_name = "build"
    job = yaml_utilities.get_job_context_for_name(
        ad_parser, ADYML_FILENAME, requested_name
    )
    assert len(job.variables) == 3


def test_get_job():
    job = ad_parser.get_job(ADYML_FILENAME, "build")
    assert job.job_name == "build"
