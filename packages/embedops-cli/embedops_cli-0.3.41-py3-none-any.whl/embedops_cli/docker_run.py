"""
`docker_run`
=======================================================================
Module will take a local run context and run a job locally in Docker
* Author(s): Bailey Steinfadt
"""
# skip pylint too-many-branches and too-many-statements warnings
# pylint: disable=R0912, disable=R0915

import os
import re
import subprocess
import logging
from sys import platform, stdout
from dotenv import dotenv_values

from embedops_cli.environment_utilities import PROJECT_ENV_FILE
from embedops_cli.utilities import quote_str_for_platform
from embedops_cli import environment_utilities as envutil
from embedops_cli.embedops_authorization import get_registry_token, user_secrets
from .eo_types import (
    NoDockerContainerException,
    InvalidDockerContainerException,
    DockerImageForBootstrapNotFound,
    DockerNotRunningException,
    DockerRegistryException,
    LocalRunContext,
    SshDirDoesNotExistException,
    SshDirIsNotADirectoryException,
)

# print ascii embedops logo from docker run scripts in git bash without issue
stdout.reconfigure(encoding="utf-8")


MAX_CONTAINER_NAME_LENGTH = 30
DOCKER_DOMAIN = "623731379476.dkr.ecr.us-west-2.amazonaws.com"
_logger = logging.getLogger(__name__)


def _remove_special_char(string):
    """
    Remove special characters from the input string.
    """
    # Make an RE character set and pass it as an argument
    # into the compile function
    string_check = re.compile("[~`!@#$%^&*()+=}{\\[\\]|\\\\:;\"'<>?/,]")

    # Remove the special characters
    clean_string = string_check.sub("", string)

    return clean_string


def _clean_job_name(job_name):
    """
    Remove special characters, spaces from the input job name string,
    and truncate it if necessarily.
    """
    # Checkpoint 1: Check for disallowed characters and remove them.
    # Allowed characters: [a-zA-Z0-9][a-zA-Z0-9_.-]
    clean_job_name = _remove_special_char(job_name)

    # Remove spaces
    clean_job_name = clean_job_name.replace(" ", "")

    # Checkpoint 2: Check for the string length and truncate it if necessarily.
    # Container name can only be up to 30 characters long
    if len(clean_job_name) > MAX_CONTAINER_NAME_LENGTH:
        clean_job_name = clean_job_name[0:MAX_CONTAINER_NAME_LENGTH]

    return clean_job_name


def _exec_dockercmd(dockercmd):
    _logger.debug(" ".join(dockercmd))

    _rc = None

    try:
        with subprocess.Popen(
            " ".join(dockercmd), shell=True, stdout=subprocess.PIPE
        ) as process:
            while True:
                output = process.stdout.readline()
                # used to check for empty output in Python2, but seems
                # to work with just poll in 2.7.12 and 3.5.2
                # if output == '' and process.poll() is not None:
                if process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode())
        _rc = process.poll()
    except subprocess.CalledProcessError as err:
        _logger.error(f"Subprocess returned an error: {err}")
        # TODO: figure out how to use click to return these to the user
        # and logger to return things to the devs.
        try:
            print(err.stdout.decode("utf-8"))
        except UnicodeDecodeError as decode_err:
            _logger.error(decode_err)
        _logger.error(err.returncode)

        if "Is the docker daemon running?" in str(err.stdout):
            raise DockerNotRunningException from err
        if "Unable to find image" in str(err.stdout):
            raise DockerRegistryException from err

        return err.returncode
    finally:
        envutil.delete_job_env_file()
    return _rc


# TODO: check that we have a script, docker_tag, and job_name
# TODO: add exceptions to eo_types and raise in here for different issues
def _create_docker_command(
    run_context: LocalRunContext, docker_cache: bool, secrets_file: str
):

    _handle_docker_tag(run_context)

    # We're assuming the tool is run from the same directory as the CI YAML
    _pwd = (
        os.getcwd().replace("\\", "\\\\")
        if platform in ("win32", "cygwin")
        else os.getcwd()
    )
    container_name = _clean_job_name(run_context.job_name)

    _logger.debug(f"Current working directory: {_pwd}")
    _logger.debug(f"Clean container name: {container_name}")

    script = ";".join(run_context.script)

    _logger.debug(f"Script as string: {script}")

    # add AWS credential for DinD
    aws_token_data = get_registry_token(secrets_file=secrets_file)
    aws_token_data["AWS_ACCESS_KEY_ID"] = aws_token_data.pop("registry_token_id")
    aws_token_data["AWS_SECRET_ACCESS_KEY"] = aws_token_data.pop(
        "registry_token_secret"
    )
    run_context.variables.update(aws_token_data)

    envutil.create_job_env_file(run_context.variables)

    dockercmd = ["docker", "run", "--rm"]
    if not docker_cache:
        dockercmd.extend(["--pull=always"])

    if os.path.exists(envutil.JOB_ENV_FILE):
        dockercmd.extend([f"--env-file={envutil.JOB_ENV_FILE}"])

    _handle_ssh(dockercmd)

    quoted_script = quote_str_for_platform(script)

    # remove embedops-azure-run if found
    pattern = r"embedops-azure-run \"(.*?)\""
    results = re.search(pattern, quoted_script)
    if results:
        quoted_script = f"'{results.group(1)}'"

    _docker_run_cmd_arg = f"/bin/bash -l -c -e {quoted_script}"

    dockercmd.extend(
        [
            "--name",
            container_name,
            "-v",
            f"{_pwd}:/eo_workdir",
            "-w",
            "/eo_workdir",
            "-e",
            f"EO_WORKDIR={_pwd}",
            "-v",
            "/var/run/docker.sock:/var/run/docker.sock",
        ]
        + (
            ["-e", "LOCAL_UID=$(id -u $USER)", "-e", "LOCAL_GID=$(id -g $USER)"]
            if platform in ("linux", "linux2")
            # env var set by CLI and used by EmbedOps image
            # entrypoint to handle local permissions for non-linux OS
            else [
                "-e",
                "LINUX=0",
            ]
        )
        + [
            "-i",
            run_context.docker_tag,
            _docker_run_cmd_arg,
        ]
    )
    return dockercmd


def docker_run(run_context: LocalRunContext, docker_cache: bool):
    """Takes a run context and launches Docker with the parameters"""
    dockercmd = _create_docker_command(
        run_context, docker_cache, secrets_file=user_secrets
    )
    return _exec_dockercmd(dockercmd)


def _handle_docker_tag(run_context: LocalRunContext):
    if run_context.docker_tag is None:
        raise DockerImageForBootstrapNotFound()

    if run_context.docker_tag == "":
        raise NoDockerContainerException()

    if "http://" in run_context.docker_tag:
        raise InvalidDockerContainerException()


def _handle_ssh(dockercmd):
    embedops_ssh_dir = dotenv_values(PROJECT_ENV_FILE).get("EMBEDOPS_SSH_DIR")
    # grab ssh config and keys for any git related work
    if embedops_ssh_dir:
        # bind mount specified directory into /tmp/.ssh (which is later copied in entrypoint.sh)
        _logger.debug(f"EMBEDOPS_SSH_DIR {embedops_ssh_dir}")
        ssh_dir = os.path.expanduser(embedops_ssh_dir)
        if not os.path.exists(ssh_dir):
            raise SshDirDoesNotExistException
        if not os.path.isdir(ssh_dir):
            raise SshDirIsNotADirectoryException
        dockercmd.extend([f"-v {ssh_dir}:/tmp/.ssh"])
    else:
        # bind-mount host user's ~/.ssh directory
        dockercmd.extend(
            [f"-v {os.path.expanduser('~')}{os.path.sep}.ssh:/home/ci/.ssh"]
        )
