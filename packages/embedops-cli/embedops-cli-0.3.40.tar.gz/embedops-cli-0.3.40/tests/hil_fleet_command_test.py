import os
import re
import pytest
from click.testing import CliRunner
from tests.utilities.fake_repo import FakeRepo
from embedops_cli import embedops_cli
from embedops_cli.api.rest import ApiException

TEST_REPO_ID = '5040a275-ff9e-449d-8b91-76a0d4eb4451'

ObjectGenerator = lambda **kwargs: type("Object", (), kwargs)

fake_devices = [
    ObjectGenerator(device_name="dev1", is_online=True),
    ObjectGenerator(device_name="dev2", is_online=False),
]


# Allows us to fake out the call to get_presigned_url
class MockUserClient:

    def __init__(self, status):
        self.status = status

    def get_repo_fleet_devices(self, repo_id):

        if not 200 <= self.status <= 299:
            raise ApiException(status=self.status)

        return fake_devices


@pytest.fixture(autouse=True)
def fake_repo_instance():

    """Sets up the fake repo and CLI global objects, used by the rest of the tests"""

    fake_repo_instance = FakeRepo(TEST_REPO_ID)
    current_dir = os.getcwd()
    os.chdir(fake_repo_instance.get_fake_repo_path())

    yield fake_repo_instance

    fake_repo_instance.cleanup()
    os.chdir(current_dir)


@pytest.fixture(autouse=True)
def configure_env(monkeypatch, mocker):

    """Run before every test function to set up common mocks and stubs"""

    # Patch stuff for request mocking, all to "good" returns
    # For the run command there's three network requests: getting the URL, uploading, and the SSE run command
    mocker.patch("embedops_cli.embedops_authorization.get_user_client", return_value=MockUserClient(200))
    mocker.patch("embedops_cli.config.get_repo_id", return_value='test_repo_id')

    yield


def get_fleet_result():

    """Utility function to invoke the command and return the result"""

    runner = CliRunner(mix_stderr=False)
    cli_result = runner.invoke(embedops_cli.embedops_cli, ["hil", "fleet"])
    return cli_result


def test_fleet_command_repo_id_not_found(mocker):

    """Test the result of the fleet command when the repo ID could not be found"""

    mocker.patch("embedops_cli.config.get_repo_id", return_value=None)

    cli_result = get_fleet_result()
    assert "repo id not found" in cli_result.stderr
    assert cli_result.exit_code == 2


def test_fleet_command_network_error(mocker):

    """Test the result of the fleet command when the get fleet endpoint returns != 200"""

    # Re-patch to be a bad return
    mocker.patch("embedops_cli.embedops_authorization.get_user_client", return_value=MockUserClient(404))

    cli_result = get_fleet_result()
    assert "repo id not found" in cli_result.stderr
    assert cli_result.exit_code == 2


def test_run_command_run_success():

    """Test a successful call to the fleet command"""

    cli_result = get_fleet_result()

    lines = cli_result.stdout.split('\n')
    assert len(lines) >= 2

    match_1 = re.match(r"^dev1\s*Online$", lines[0])
    match_2 = re.match(r"^dev2\s*Offline$", lines[1])

    assert match_1
    assert match_2
    assert cli_result.exit_code == 0