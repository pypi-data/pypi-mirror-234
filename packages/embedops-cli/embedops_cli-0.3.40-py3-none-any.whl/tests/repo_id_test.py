import os
import pytest
from embedops_cli.config import get_repo_id


def test_repo_id_file_does_not_exist():
    config_path = os.path.join(os.path.abspath(os.path.curdir), 'tests', 'file_fixtures', 'this_file_does_not_exist.yml')
    assert get_repo_id(config_path) is None


def test_repo_id_setting_does_not_exist():
    config_path = os.path.join(os.path.abspath(os.path.curdir), 'tests', 'file_fixtures', 'repo_id_not_exists.yml')
    assert get_repo_id(config_path) is None


def test_repo_id_setting_exists():
    config_path = os.path.join(os.path.abspath(os.path.curdir), 'tests', 'file_fixtures', 'repo_id_exists.yml')
    assert get_repo_id(config_path) == '82C2B536-3FCA-41C5-9777-5DE4B805C6D5'
