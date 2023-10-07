"""This module provides a central store for configuration data, drawing from environment variables
configuration files, and other sources as needed"""
import os
from dynaconf import Dynaconf

SETTINGS_FILES = ["settings.toml", ".secrets.toml"]
REPO_ID_PATH = os.path.join(os.path.abspath(os.path.curdir), ".embedops", "repo_id.yml")

# get an absolute path to the director that this file is in
abs_current_dir = os.path.dirname(os.path.abspath(__file__))

# prepend the settings filenames with an absolute path to the current directory
# by providing an absolute path, dynaconf will load it directly instead of
# searching for it
settings_paths = [
    os.path.join(abs_current_dir, settings_file) for settings_file in SETTINGS_FILES
]

settings = Dynaconf(
    load_dotenv=True,
    envvar_prefix="EMBEDOPS",
    environments=True,
    settings_files=settings_paths,
)

# for some reason, we have to set the loaders separately to be able to use `.configure` to
# change them for tests
settings.configure(
    LOADERS_FOR_DYNACONF=[
        "dynaconf.loaders.yaml_loader",
        "dynaconf.loaders.env_loader",
        "embedops_cli.ci_config_loader",
    ]
)


def get_repo_id(path=REPO_ID_PATH):
    """get repo_id from .embedops/repo_id.yml

    Args:
        path (string, optional):    Absolute file system path to .embedops/repo_id.yml.
                                    Defaults to REPO_ID_PATH.

    Returns:
        str: the value stored in <repo_root>/.embedops/repo_id.yml:REPO_ID or None
    """
    dot_eo = Dynaconf(
        load_dotenv=False,
        settings_files=[path],
        silent_errors=True,
    )
    dot_eo.configure(
        LOADERS_FOR_DYNACONF=[
            "dynaconf.loaders.yaml_loader",
        ]
    )
    return dot_eo.get("repo_id")
