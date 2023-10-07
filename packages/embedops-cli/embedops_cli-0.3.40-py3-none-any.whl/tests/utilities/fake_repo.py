"""Module for the FakeRepo testing utility class"""

import os
import shutil

TEST_HIL_ROOT_PATH      = 'hil'
TEST_HIL_ARTIFACTS_PATH = 'artifacts/test.hex'
TEST_ARTIFACT_SOURCE    = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "file_fixtures", "main.hex"))


class FakeRepo:

    """Creates a temporary directory that looks like a fully-functioning repository directory"""

    def __init__(self, repo_id):

        """Create the initial temporary directory"""
        self.repo_id = repo_id

        self.reset()

    def reset(self):
        """Completely reset and restore a fake repo into the same initial temporary directory"""

        # Remove temp source directory
        self.temp_dir_path = os.path.join(os.getcwd(), 'fake_repo_dir')
        shutil.rmtree(self.temp_dir_path, ignore_errors=True)

        current_path = os.path.dirname(os.path.abspath(__file__))
        fake_repo_golden_path = os.path.join(current_path, '..', 'file_fixtures', 'fake_repo_golden')

        # Copy the golden version to our existing temp path
        print(shutil.copytree(fake_repo_golden_path, self.temp_dir_path))

        self.hil_config_yml = os.path.join(self.temp_dir_path, '.embedops', 'hil', 'config.yml')

    def get_fake_repo_path(self):
        """Return the full absolute path to the fake repo"""
        return self.temp_dir_path

    def cleanup(self):
        """Cleanup all temporary files and directories"""
        shutil.rmtree(self.temp_dir_path, ignore_errors=True)

    def remove_hil_config_yml(self):
        """Delete the repo_id.yml file"""
        os.remove(self.hil_config_yml)

    def remove_hil_root_path_attr(self):
        """Invalidate the repo_id.yml file"""
        with open(self.hil_config_yml, "w") as config_file:
            config_file.write('not_hil_root_path: test\n')
            config_file.write('hil_artifacts: %s\n' % TEST_HIL_ARTIFACTS_PATH)

    def remove_hil_artifacts_path_attr(self):

        with open(self.hil_config_yml, "w") as config_file:
            config_file.write('hil_root_path: %s\n' % TEST_HIL_ROOT_PATH)
            config_file.write('not_hil_artifacts: test\n')

    def remove_artifacts_dir(self):

        shutil.rmtree(os.path.join(self.temp_dir_path, 'artifacts'), ignore_errors=True)
