"""
`docker_run_test`
=======================================================================
Unit tests for the module that takes a local run context and run a job locally in Docker
* Author(s): Zhi Xuen Lai
"""
import os
import pytest
from pathlib import Path
from embedops_cli import docker_run
from embedops_cli.yaml_tools import bb_parser, gl_parser, yaml_utilities
from embedops_cli.eo_types import (
    NoDockerContainerException,
    InvalidDockerContainerException,
    DockerImageForBootstrapNotFound,
)
from tests import BBYML_FILENAME, GLYML_FILENAME

GLYML_NO_IMAGE_FILENAME = "tests/gl-pipelines/test-no-image-.gitlab-ci.yml"
GLYML_NO_IMAGE_FOR_BOOTSTRAP_FILENAME = (
    "tests/gl-pipelines/test-no-image-for-bootstrap-.gitlab-ci.yml"
)
ADYML_NO_IMAGE_FOR_BOOTSTRAP_FILENAME = (
    "tests/ad-pipelines/test-no-image-name-for-bootstrap-azure-pipelines.yml"
)


def test_clean_bb_job_name_with_spaces():
    """Test cleaning Bitbucket job name with spaces"""
    job_name_list = bb_parser.get_job_name_list(BBYML_FILENAME)
    cleaned_job_name = ""

    for job_name in job_name_list:
        if job_name == "Step With Spaces":
            cleaned_job_name = docker_run._clean_job_name(job_name)
            break

    assert cleaned_job_name == "StepWithSpaces"


def test_clean_gl_job_name_with_spaces():
    """Test cleaning GitLab job name with spaces"""
    job_name_list = gl_parser.get_job_name_list(GLYML_FILENAME)
    cleaned_job_name = ""

    for job_name in job_name_list:
        if job_name == "Step With Spaces":
            cleaned_job_name = docker_run._clean_job_name(job_name)
            break

    assert cleaned_job_name == "StepWithSpaces"


def test_clean_bb_job_name_with_special_characters():
    """Test cleaning Bitbucket job name with special characters"""
    job_name_list = bb_parser.get_job_name_list(BBYML_FILENAME)
    cleaned_job_name = ""

    for job_name in job_name_list:
        if job_name == "~Step@With$Special>Char?":
            cleaned_job_name = docker_run._clean_job_name(job_name)
            break

    assert cleaned_job_name == "StepWithSpecialChar"


def test_clean_gl_job_name_with_special_characters():
    """Test cleaning GitLab job name with special characters"""
    job_name_list = gl_parser.get_job_name_list(GLYML_FILENAME)
    cleaned_job_name = ""

    for job_name in job_name_list:
        if job_name == "~Step@With$Special>Char?":
            cleaned_job_name = docker_run._clean_job_name(job_name)
            break

    assert cleaned_job_name == "StepWithSpecialChar"


def test_clean_bb_job_name_with_too_many_characters():
    """Test cleaning Bitbucket job name with too many characters"""
    job_name_list = bb_parser.get_job_name_list(BBYML_FILENAME)
    cleaned_job_name = ""

    for job_name in job_name_list:
        if job_name == "StepWithNameMoreThanThirtyCharacters":
            cleaned_job_name = docker_run._clean_job_name(job_name)
            break

    assert cleaned_job_name == "StepWithNameMoreThanThirtyChar"


def test_clean_gl_job_name_with_too_many_characters():
    """Test cleaning GitLab job name with too many characters"""
    job_name_list = gl_parser.get_job_name_list(GLYML_FILENAME)
    cleaned_job_name = ""

    for job_name in job_name_list:
        if job_name == "StepWithNameMoreThanThirtyCharacters":
            cleaned_job_name = docker_run._clean_job_name(job_name)
            break

    assert cleaned_job_name == "StepWithNameMoreThanThirtyChar"


def test_clean_bb_job_name_with_all_restrictions():
    """Test cleaning Bitbucket job name with all restrictions"""
    job_name_list = bb_parser.get_job_name_list(BBYML_FILENAME)
    cleaned_job_name = ""

    for job_name in job_name_list:
        if (
            job_name
            == "Step% :With;&= All++([{Restrictions}])That* You> Can> |Imagine|!"
        ):
            cleaned_job_name = docker_run._clean_job_name(job_name)
            break

    assert cleaned_job_name == "StepWithAllRestrictionsThatYou"


def test_clean_gl_job_name_with_all_restrictions():
    """Test cleaning GitLab job name with all restrictions"""
    job_name_list = gl_parser.get_job_name_list(GLYML_FILENAME)
    cleaned_job_name = ""

    for job_name in job_name_list:
        if (
            job_name
            == "Step% :With;&= \\All++([{Restrictions}])That* You> Can> |Imagine|!"
        ):
            cleaned_job_name = docker_run._clean_job_name(job_name)
            break

    assert cleaned_job_name == "StepWithAllRestrictionsThatYou"


def test_clean_bb_job_name_with_valid_name():
    """Test cleaning Bitbucket job name with valid name"""
    job_name_list = bb_parser.get_job_name_list(BBYML_FILENAME)
    cleaned_job_name = ""

    for job_name in job_name_list:
        if job_name == "St3p_W1th-Val1d.Nam3":
            cleaned_job_name = docker_run._clean_job_name(job_name)
            break

    assert cleaned_job_name == "St3p_W1th-Val1d.Nam3"


def test_clean_gl_job_name_with_valid_name():
    """Test cleaning GitLab job name with valid name"""
    job_name_list = gl_parser.get_job_name_list(GLYML_FILENAME)
    cleaned_job_name = ""

    for job_name in job_name_list:
        if job_name == "St3p_W1th-Val1d.Nam3":
            cleaned_job_name = docker_run._clean_job_name(job_name)
            break

    assert cleaned_job_name == "St3p_W1th-Val1d.Nam3"


def test_docker_run_without_image():
    """Test running a job with invalid image"""
    job_list = gl_parser.get_job_list(GLYML_NO_IMAGE_FILENAME)

    for job in job_list:
        if job.job_name == "StepWithoutImage":
            with pytest.raises(NoDockerContainerException):
                assert docker_run.docker_run(job, False)
            break


def test_docker_run_with_invalid_image():
    """Test running a job with invalid image"""
    job_list = gl_parser.get_job_list(GLYML_FILENAME)

    for job in job_list:
        if job.job_name == "StepWithInvalidImage":
            with pytest.raises(InvalidDockerContainerException):
                assert docker_run.docker_run(job, False)
            break


def test_gl_docker_run_with_missing_image_for_bootstrap():
    """Test running a job for Gitlab with no image specified for a bootstrap"""
    job_list = yaml_utilities.get_job_list(GLYML_NO_IMAGE_FOR_BOOTSTRAP_FILENAME)

    for job in job_list:
        if job.job_name == "StepWithoutImageForBoostrap":
            with pytest.raises(DockerImageForBootstrapNotFound):
                assert docker_run.docker_run(job, False)
            break


def test_ad_docker_run_with_missing_image_for_bootstrap():
    """Test running a job for Azure with no image specified for a bootstrap"""
    job_list = yaml_utilities.get_job_list(ADYML_NO_IMAGE_FOR_BOOTSTRAP_FILENAME)

    for job in job_list:
        if job.job_name == "StepWithoutImageForBoostrap":
            with pytest.raises(DockerImageForBootstrapNotFound):
                assert docker_run.docker_run(job, False)
            break


def test_pull_always_in_dockercmd():
    job_list = gl_parser.get_job_list(GLYML_FILENAME)
    for job in job_list:
        if job.job_name == "StepWithNamedImage":
            cmd = docker_run._create_docker_command(
                run_context=job,
                docker_cache=False,
                secrets_file=os.path.join(Path(__file__).parent, 'file_fixtures', 'mock-eosecrets.toml')
            )
            assert "--pull=always" in cmd
            break


def test_pull_always_not_in_dockercmd():
    job_list = gl_parser.get_job_list(GLYML_FILENAME)
    for job in job_list:
        if job.job_name == "StepWithNamedImage":
            cmd = docker_run._create_docker_command(
                run_context=job,
                docker_cache=True,
                secrets_file=os.path.join(Path(__file__).parent, 'file_fixtures', 'mock-eosecrets.toml')
            )
            assert "--pull=always" not in cmd
            break
