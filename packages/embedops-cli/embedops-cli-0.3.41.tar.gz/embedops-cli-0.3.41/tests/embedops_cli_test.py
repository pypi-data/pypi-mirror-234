"""
`embedops_cli_test`
=======================================================================
Unit tests for the CLI interface for EmbedOps tools
* Author(s): Bailey Steinfadt
"""

import os
import pytest
import shutil
from click.testing import CliRunner
from embedops_cli import embedops_cli
from tests import BBYML_FILENAME, GLYML_FILENAME
from embedops_cli.config import settings
from embedops_cli.eo_types import (
    UnauthorizedUserException,
    NoDockerCLIException,
    DockerNotRunningException,
)

NOT_A_FILENAME = "not_a_file.yaml"
GHYML_TEST_DETECTION_FILENAME = "gh-pipelines/.github/workflows/test-detection-.github-ci.yml"


@pytest.fixture(autouse=True)
def configure_env(monkeypatch, mocker):
    monkeypatch.setenv("EMBEDOPS_HOST", "https://dev-01.embedops.io")
    settings.host = "https://dev-01.embedops.io:443"


@pytest.fixture(scope="session")
def change_test_dir(request):
    """
    A function-level fixture that changes to the test case directory,
    run the test (yield), then change back to the calling directory to
    avoid side-effects.
    """
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)


def test_version_command():
    """Learned how to write tests for click by testing build in version command"""
    runner = CliRunner()
    result = runner.invoke(embedops_cli.embedops_cli, ["--version"])
    assert result.exit_code == 0
    assert result.output[:21] == "embedops-cli, version"


def test_help_command():
    """Learned how to write tests for click by testing built in help command"""
    runner = CliRunner()
    h_result = runner.invoke(embedops_cli.embedops_cli, "-h")
    assert h_result.exit_code == 0
    help_result = runner.invoke(embedops_cli.embedops_cli, "--help")
    assert help_result.exit_code == 0
    assert help_result.output == h_result.output
    halp_result = runner.invoke(embedops_cli.embedops_cli, "--halp")
    assert halp_result.exit_code == 0
    assert halp_result.output == h_result.output


def test_jobs_command():
    """Test the top level jobs group"""
    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli, ["jobs", "--filename", "not_a_file.yaml"]
    )
    assert result.exit_code == 2


def test_show_jobs_no_filename():
    """Test the show job list command no filename"""
    runner = CliRunner()
    result = runner.invoke(embedops_cli.embedops_cli, ["jobs", "show"])
    assert result.exit_code == 0


def test_show_jobs_nonexistent_filename():
    """Test the show job list command with a nonexistent file"""
    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli, ["jobs", "--filename", "not_a_file.yaml", "show"]
    )
    assert result.exit_code == 2


def test_show_jobs_not_yaml_filename():
    """Test the show job list command with a non-yaml filename"""
    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli, ["jobs", "--filename", "tests/README.md", "show"]
    )
    assert result.exit_code == 1


def test_show_jobs():
    """Test the show job list command correct syntax"""
    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli,
        ["jobs", "--filename", BBYML_FILENAME, "show"],
    )
    assert result.exit_code == 0

    result = runner.invoke(
        embedops_cli.embedops_cli,
        ["jobs", "--filename", GLYML_FILENAME, "show"],
    )
    assert result.exit_code == 0


def test_run_jobs_no_job_name_or_filename():
    """Test the run job command with no job or filename"""

    runner = CliRunner()
    result = runner.invoke(embedops_cli.embedops_cli, ["jobs", "run"])
    assert result.exit_code == 2


def test_run_jobs_no_job_name():
    """Test the run job list command with no job name"""
    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli,
        ["jobs", "--filename", BBYML_FILENAME, "run"],
    )
    assert result.exit_code == 2


def test_run_jobs_nonexistent_file():
    """Test the run job command with a nonexistent file"""
    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli,
        ["jobs", "--filename", NOT_A_FILENAME, "run", "build"],
    )
    assert result.exit_code == 2


def test_run_jobs_not_yaml_filename():
    """Test the run job command with a non-yaml filename"""
    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli,
        ["jobs", "--filename", "tests/README.md", "run", "build"],
    )
    assert result.exit_code == 1


def test_stale_token_prompts_login(mocker):
    """Test that a no-longer-valid auth token prompts"""
    docker_status = mocker.patch(
        "embedops_cli.embedops_cli.docker_is_installed_and_running"
    )
    docker_status.return_value = True

    token_status = mocker.patch(
        "embedops_cli.embedops_cli.embedops_authorization.check_token"
    )
    token_status.return_value = False

    do_login = mocker.patch(
        "embedops_cli.embedops_cli.embedops_authorization.request_authorization"
    )
    do_login.side_effect = UnauthorizedUserException()
    runner = CliRunner()
    result = runner.invoke(embedops_cli.embedops_cli, "login")
    do_login.assert_called()

    assert result.exit_code != 0

    # mock `check user` to return false
    # verify that "do login" is called
    # verify that if "do login" is successful that the return value is 0


def test_docker_not_found(mocker):
    """Test docker command was not found"""
    docker_status = mocker.patch("embedops_cli.embedops_cli.subprocess.check_output")
    docker_status.side_effect = NoDockerCLIException()

    token_status = mocker.patch(
        "embedops_cli.embedops_cli.embedops_authorization.check_token"
    )
    runner = CliRunner()
    result = runner.invoke(embedops_cli.embedops_cli, "login")
    token_status.assert_not_called()

    assert result.exit_code != 0


def test_docker_not_running(mocker):
    """Test when docker is not running"""
    docker_status = mocker.patch("embedops_cli.embedops_cli.subprocess.check_output")
    docker_status.side_effect = DockerNotRunningException()

    token_status = mocker.patch(
        "embedops_cli.embedops_cli.embedops_authorization.check_token"
    )
    runner = CliRunner()
    result = runner.invoke(embedops_cli.embedops_cli, "login")
    token_status.assert_not_called()

    assert result.exit_code != 0


# turn off for CI as docker cannot be run there
# def test_gh_run_happy():
#     """run the happy path, actually runs cppcheck but just exits 0"""
#     test_file_path = 'tests/.github/workflows/embedops.yml'
#     shutil.copyfile('tests/.github/workflows/happy.yml', test_file_path)

#     runner = CliRunner()
#     result = runner.invoke(
#         embedops_cli.embedops_cli,
#         ["jobs", "--filename", test_file_path, "run", "Cppcheck"],
#     )
#     print(f'result: {result.stdout}')
#     os.remove(test_file_path)
#     assert result.exit_code == 0


def test_gh_run_jobs_no_env_embedops_image():
    """validate bad exit when no env vars defined in build step"""
    test_file_path = 'tests/gh-pipelines/.github/workflows/embedops.yml'
    shutil.copyfile('tests/gh-pipelines/.github/workflows/no_env_embedops_image.yml', test_file_path)

    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli,
        ["jobs", "--filename", test_file_path, "run", "Cppcheck"],
    )
    print(f'result: {result.stdout}')
    os.remove(test_file_path)
    assert result.exit_code == 1


def test_gh_run_jobs_no_with_args():
    """validate bad exit when no with.args defined in build step"""
    test_file_path = 'tests/gh-pipelines/.github/workflows/embedops.yml'
    shutil.copyfile('tests/gh-pipelines/.github/workflows/no_with_args.yml', test_file_path)

    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli,
        ["jobs", "--filename", test_file_path, "run", "Cppcheck"],
    )
    os.remove(test_file_path)
    assert result.exit_code != 0


def test_gh_run_jobs_no_uses_stanza():
    """validate bad exit when no uses clause in build step"""
    test_file_path = 'tests/gh-pipelines/.github/workflows/embedops.yml'
    shutil.copyfile('tests/gh-pipelines/.github/workflows/no_uses.yml', test_file_path)

    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli,
        ["jobs", "--filename", test_file_path, "run", "Cppcheck"],
    )
    os.remove(test_file_path)
    assert result.exit_code == 1


def test_gh_run_jobs_uses_no_docker():
    """validate bad exit when the bootstrap uses clause isn't prefixed correctly"""
    test_file_path = 'tests/gh-pipelines/.github/workflows/embedops.yml'
    shutil.copyfile('tests/gh-pipelines/.github/workflows/uses_no_docker.yml', test_file_path)

    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli,
        ["jobs", "--filename", test_file_path, "run", "Cppcheck"],
    )
    print(f'result: {result.stdout}')
    os.remove(test_file_path)
    assert result.exit_code == 1


def test_gh_run_jobs_no_job_name():
    """validate bad exit when using legacy style pipeline yaml for GH"""
    test_file_path = 'tests/gh-pipelines/.github/workflows/embedops.yml'
    shutil.copyfile('tests/'+GHYML_TEST_DETECTION_FILENAME, test_file_path)

    runner = CliRunner()
    result = runner.invoke(
        embedops_cli.embedops_cli,
        ["jobs", "--filename", test_file_path, "run"],
    )
    os.remove(test_file_path)
    assert result.exit_code == 2
