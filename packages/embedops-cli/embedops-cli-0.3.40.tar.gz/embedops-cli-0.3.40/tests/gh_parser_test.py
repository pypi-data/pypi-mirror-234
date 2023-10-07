"""
`gl_parser_test`
=======================================================================
Unit tests for the parser to pull job contexts from .gitlab-ci.yml files
* Author(s): Bailey Steinfadt
"""
import os
import pytest
import shutil
from embedops_cli.yaml_tools import gh_parser, yaml_utilities
from embedops_cli.eo_types import BadYamlFileException
from tests import GHYML_FILENAME


GHYML_INVALID_INDENTATION_FILENAME = "tests/gh-pipelines/test-invalid-indentation-.github-ci.yml"
GHYML_INVALID_JOB_NAME_FILENAME = "tests/gh-pipelines/test-invalid-job-name-.github-ci.yml"
GHYML_NO_STEPS_FILENAME = "tests/gh-pipelines/test-no-steps-.github-ci.yml"


def test_get_job_list_with_invalid_indentation_exception():
    """test that exception is raised for job with invalid indentation"""
    with pytest.raises(BadYamlFileException):
        assert gh_parser.get_job_list(GHYML_INVALID_INDENTATION_FILENAME)


def test_get_job_list_with_invalid_name_exception():
    """test that exception is raised for job with invalid name"""
    with pytest.raises(BadYamlFileException):
        assert gh_parser.get_job_list(GHYML_INVALID_JOB_NAME_FILENAME)


def test_get_job_list_without_steps_exception():
    """test that exception is raised for job without steps section"""
    with pytest.raises(BadYamlFileException):
        assert gh_parser.get_job_list(GHYML_NO_STEPS_FILENAME)


def test_get_job_list():
    """Test retrieving the list of complete local run context from the YAML"""
    job_list = gh_parser.get_job_list(GHYML_FILENAME)
    print(job_list)
    assert len(job_list) >= 3
    filtered_job_list = [
        job for job in job_list if job.job_name == "JobContainsOnlyLetters"
    ]
    assert len(filtered_job_list) == 1
    print(f'filtered_job_list: {filtered_job_list}')
    print(f'filtered_job_list[0]: {filtered_job_list[0]}')
    print(f'filtered_job_list[0].docker_tag: {filtered_job_list[0].docker_tag}')
    assert (
        filtered_job_list[0].docker_tag
        == "docker://public.ecr.aws/embedops/github-bootstrap:1.0"
    )
    assert filtered_job_list[0].script[0] == 'echo "Job contains only letters"'


def test_get_job_name_list_with_invalid_indentation_exception():
    """test that exception is raised for job with invalid indentation"""
    with pytest.raises(BadYamlFileException):
        assert gh_parser.get_job_name_list(GHYML_INVALID_INDENTATION_FILENAME)


def test_get_job_name_list_with_invalid_name_exception():
    """test that exception is raised for job with invalid name"""
    with pytest.raises(BadYamlFileException):
        assert gh_parser.get_job_name_list(GHYML_INVALID_JOB_NAME_FILENAME)


def test_get_job_name_list():
    """Test retrieving the list of job names from the YAML"""
    job_name_list = gh_parser.get_job_name_list(GHYML_FILENAME)
    assert len(job_name_list) >= 3
    assert (
        len(
            [
                job_name
                for job_name in job_name_list
                if job_name == "JobContainsOnlyLetters"
            ]
        )
        == 1
    )
    assert (
        len(
            [
                job_name
                for job_name in job_name_list
                if job_name == "_Job_Starts_With_Underscore"
            ]
        )
        == 1
    )
    assert (
        len(
            [
                job_name
                for job_name in job_name_list
                if job_name == "Job-Separated-By-Dash"
            ]
        )
        == 1
    )


def test_get_job_context():
    """Test getting the job context for an indicated job"""
    requested_name = "Job_Contains-A1123Valid-Characters"
    job = yaml_utilities.get_job_context_for_name(
        gh_parser, GHYML_FILENAME, requested_name
    )
    assert job.job_name == requested_name


def test_get_pipeline_variables():
    """Test getting variables defined outside of job definitions"""
    job_list = gh_parser.get_job_list(GHYML_FILENAME)
    job = [job for job in job_list if job.job_name == "Job1Contains2Numbers34567890"][0]
    # The job only has access to the PROJ_DIR variable
    assert "PROJ_DIR" in job.variables
    assert "MY_VAR" not in job.variables
    assert "MY_SUB_VAR" not in job.variables


def test_get_job_variables():
    """Test getting variables defined in a job"""
    job_list = gh_parser.get_job_list(GHYML_FILENAME)
    job = [job for job in job_list if job.job_name == "JobWithEnvVariable"][0]
    # The job only has access to the PROJ_DIR and MY_VAR variables
    assert "PROJ_DIR" in job.variables
    assert "MY_VAR" in job.variables
    assert "MY_SUB_VAR" not in job.variables


def test_get_step_variables():
    """Test getting variables defined in a step"""
    job_list = gh_parser.get_job_list(GHYML_FILENAME)
    job = [job for job in job_list if job.job_name == "JobWithStepLevelEnvVariable"][0]
    # The job only has access to the PROJ_DIR and MY_SUB_VAR variables
    assert "PROJ_DIR" in job.variables
    assert "MY_VAR" not in job.variables
    assert "MY_SUB_VAR" in job.variables


def test_job_with_run_in_sub_step():
    """Test getting run command defined in a sub-step"""
    job_list = gh_parser.get_job_list(GHYML_FILENAME)
    job = [job for job in job_list if job.job_name == "JobWithRunInSubstep"][0]
    assert job.script[0] == 'echo "Job with run in sub-step"'


def test_job_with_literal_multiline_block():
    """Test retrieving a literal multiline block"""
    job = yaml_utilities.get_job_context_for_name(
        gh_parser, GHYML_FILENAME, "JobWithLiteralMultilineBlock"
    )
    assert (
        job.script[0]
        == 'FILE=.clang-format\nif [ -f "$FILE" ]; then echo "$FILE exists. Use repository $FILE."; else echo "$FILE does not exist. Use container $FILE."; cp /tools/.clang-format .clang-format; fi\n'
    )


def test_step_with_folded_multiline_block():
    """Test retrieving a folded multiline block"""
    job = yaml_utilities.get_job_context_for_name(
        gh_parser, GHYML_FILENAME, "JobWithFoldedMultilineBlock"
    )
    assert (
        job.script[0]
        == 'FILE=.clang-format\nif [ -f "$FILE" ]; then echo "$FILE exists. Use repository $FILE."; else echo "$FILE does not exist. Use container $FILE."; cp /tools/.clang-format .clang-format; fi\n'
    )


def test_gh_style_context_variables():
    """ validate that GH parsing ignores all Github-style context variables """
    yml = """
name: EmbedOps

on:
  workflow_dispatch:
  push:
    branches:
      - master

jobs:
  test:
    name: test
    runs-on: ubuntu-latest
    steps:
      - name: Create cppcheck report
        uses: docker://public.ecr.aws/embedops/github-bootstrap:1.0
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          EMBEDOPS_API_REPO_KEY: ${{ secrets.EMBEDOPS_API_REPO_KEY }}
          SOME_STRANGE_REPO_VARIABLE: ${{foo.BAR}}
          EMBEDOPS_IMAGE: "cppcheck:2.8"
          EMBEDOPS_JOB_NAME: "cppcheck-2.8"
          EMBEDOPS_HOST: https://dev-01.embedops.io
        with:
          args:
            embedops-quality-cppcheck
"""
    with open('tests/file_fixtures/embedops.yml', 'w+') as tmp_file:
        tmp_file.write(yml)
    ctx = gh_parser.get_job_list('tests/file_fixtures/embedops.yml')
    assert ctx[0].variables.get('AWS_ACCESS_KEY_ID') is None
    assert ctx[0].variables.get('AWS_SECRET_ACCESS_KEY') is None
    assert ctx[0].variables.get('EMBEDOPS_API_REPO_KEY') is None
    assert ctx[0].variables.get('SOME_STRANGE_REPO_VARIABLE') is None
    assert ctx[0].variables.get('EMBEDOPS_HOST') is not None
    os.remove('tests/file_fixtures/embedops.yml')


def test_get_job():
    pipeline_file = 'tests/gh-pipelines/.github/workflows/embedops.yml'
    shutil.copy('tests/gh-pipelines/.github/workflows/happy.yml', pipeline_file)
    job = yaml_utilities.get_job(
        pipeline_file, "Cppcheck"
    )
    assert job.job_name == "Cppcheck"
    os.remove(pipeline_file)
