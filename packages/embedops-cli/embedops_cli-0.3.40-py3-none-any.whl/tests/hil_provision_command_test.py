import os
import fs
import pytest
import requests
from click.testing import CliRunner
from tests.utilities.fake_repo import FakeRepo
from embedops_cli import embedops_cli
from embedops_cli.api.rest import ApiException

# To create the mock image files for this test, I used the macOS disk image utility to create DMG files
# Then used this command: hdiutil convert -format UFBI -o eohil.img eohil2.dmg
# To convert to IMG

TEST_REPO_ID = '5040a275-ff9e-449d-8b91-76a0d4eb4451'

# Paths to test images.
IMAGE_ROOT            = os.path.join(os.path.dirname(__file__), 'file_fixtures')
TEST_DEVICE_CONFIG = "test_device_config"

ObjectGen = lambda **kwargs: type("Object", (), kwargs)


# mock functions for returning the upload status
def mock_get_download_response_200(url, headers=None, data=None, stream=True, timeout=10):

    # Use the URL as a file path, allowing each changing of the downloaded image
    image_path = os.path.join(IMAGE_ROOT, url)
    image_bytes = open(image_path, "rb").read()
    return ObjectGen(status_code=200, ok=True, content=image_bytes)


def mock_get_download_response_401(url, headers=None, data=None, stream=True, timeout=10):
    return ObjectGen(status_code=401, ok=False)


# Allows us to fake out calls to the Swagger code
class MockUserClient:

    def __init__(self, url_status=200, image_url="image_good.img", provision_status=200, provision_str=TEST_DEVICE_CONFIG):
        self.url_status = url_status
        self.image_url = image_url
        self.provision_status = provision_status
        self.provision_str = provision_str

    def get_latest_gateway_image_url(self):

        if self.url_status != 200:
            raise ApiException(status=self.url_status)
        return ObjectGen(url=self.image_url)

    def hil_provision_device(self, repo_id):
        if self.provision_status != 200:
            raise ApiException(status=self.provision_status)
        return ObjectGen(device_name="D-1", device_config=self.provision_str)


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
    mocker.patch("embedops_cli.embedops_authorization.get_auth_token", return_value='some_value')
    monkeypatch.setattr(requests, "get", mock_get_download_response_200)
    mocker.patch("embedops_cli.embedops_authorization.get_user_client", return_value=MockUserClient())
    mocker.patch("embedops_cli.config.get_repo_id", return_value='test_repo_id')

    yield


def get_provision_result():

    """Utility function to invoke the command and return the result"""

    runner = CliRunner(mix_stderr=False)
    cli_result = runner.invoke(embedops_cli.embedops_cli, ["hil", "provision"])
    return cli_result


def test_provision_command_repo_id_not_found(mocker):

    """Test the result of the run command when the repo ID could not be found"""

    mocker.patch("embedops_cli.config.get_repo_id", return_value=None)

    cli_result = get_provision_result()
    assert "repo id not found" in cli_result.stderr
    assert cli_result.exit_code == 2


def test_provision_command_get_image_error(mocker):

    """Test the result of the run command when the get image URL endpoint returns != 200"""

    # Re-patch to be a bad return
    mocker.patch("embedops_cli.embedops_authorization.get_user_client", return_value=MockUserClient(url_status=404))

    cli_result = get_provision_result()
    assert "network exception: 404" in cli_result.stderr
    assert cli_result.exit_code == 2


def test_provision_command_download_error(monkeypatch):

    """Test the result of the run command when the download URL endpoint returns != 200"""

    # Re-patch to be a bad return
    monkeypatch.setattr(requests, "get", mock_get_download_response_401)

    cli_result = get_provision_result()
    assert "network exception: 401" in cli_result.stderr
    assert cli_result.exit_code == 2


def test_provision_command_provision_error(mocker):

    """Test the result of the run command when the provision URL endpoint returns != 200"""

    # Re-patch to be a bad return
    mocker.patch("embedops_cli.embedops_authorization.get_user_client", return_value=MockUserClient(provision_status=404))

    cli_result = get_provision_result()
    assert "network exception: 404" in cli_result.stderr
    assert cli_result.exit_code == 2


def test_provision_command_bad_image_status(mocker):

    """Test the result of the run command when the downloaded image has a bad status"""

    # Re-patch to be a bad return
    mocker.patch("embedops_cli.embedops_authorization.get_user_client", return_value=MockUserClient(image_url='image_bad_status.img'))

    cli_result = get_provision_result()
    assert "The gateway image file could not be configured" in cli_result.stderr
    assert cli_result.exit_code == 2


def test_provision_command_bad_image_size(mocker):

    """Test the result of the run command when the downloaded image has a bad status"""

    # Re-patch to be a bad return
    mocker.patch("embedops_cli.embedops_authorization.get_user_client", return_value=MockUserClient(image_url='image_bad_size.img'))

    cli_result = get_provision_result()
    assert "The gateway image file could not be configured" in cli_result.stderr
    assert cli_result.exit_code == 2


def test_provision_command_bad_image_type(mocker):

    """Test the result of the run command when the downloaded image has a bad status"""

    # Re-patch to be a bad return
    mocker.patch("embedops_cli.embedops_authorization.get_user_client", return_value=MockUserClient(image_url='image_bad_type.img'))

    cli_result = get_provision_result()
    assert "The gateway image file could not be configured" in cli_result.stderr
    assert cli_result.exit_code == 2


def test_provision_command_success(fake_repo_instance):

    """Test the result of the run command when the presigned URL endpoint returns != 200"""

    # Do all of the legwork required to verify the correct config string was written
    MBR_SIZE_BYTES = 512
    SECTOR_SIZE_BYTES = 512

    cli_result = get_provision_result()

    # Do the legwork required to read what was actually written to the config.json file within the image
    image_path = os.path.abspath(os.path.join(fake_repo_instance.get_fake_repo_path(), 'embedops-gateway-image.img'))

    with open(image_path, "rb") as image_file:
        mbr_data = image_file.read(MBR_SIZE_BYTES)

    assert len(mbr_data) == MBR_SIZE_BYTES

    boot_partition_offset = int.from_bytes(mbr_data[454:458], byteorder="little") * SECTOR_SIZE_BYTES
    boot_fs = fs.open_fs(f"fat://{image_path}?offset={boot_partition_offset}")
    config_file = boot_fs.open("config.json", "r")
    actual_config_str = str(config_file.read())

    assert actual_config_str == TEST_DEVICE_CONFIG
    assert "Please complete provisioning" in cli_result.stdout
    assert cli_result.exit_code == 0
