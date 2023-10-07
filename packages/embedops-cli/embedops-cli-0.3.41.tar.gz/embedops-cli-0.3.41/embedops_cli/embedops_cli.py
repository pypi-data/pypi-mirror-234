"""
`embedops_cli`
=======================================================================
CLI interface for EmbedOps tools
* Author(s): Bailey Steinfadt
"""
# skip pylint subprocess-run-check because we *are* checking the exit status
# pylint: disable=W1510
import sys
import logging
import platform
import subprocess
import os
from datetime import datetime
import click
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from embedops_cli.config import get_repo_id
from embedops_cli.utilities import echo_error_and_fix

# import embedops_cli.yaml_tools.yaml_utilities as yaml_utilities
from embedops_cli.yaml_tools import yaml_utilities
from embedops_cli.hil import hil_commands
from . import docker_run, version, embedops_authorization, telemetry
from .eo_types import (
    BadYamlFileException,
    NoDockerCLIException,
    DockerNotRunningException,
    EmbedOpsException,
    LoginFailureException,
    NoYamlFileException,
    UnsupportedYamlTypeException,
    MultipleYamlFilesException,
    NoDockerContainerException,
    InvalidDockerContainerException,
    UnauthorizedUserException,
    DockerRegistryException,
    UnknownDockerException,
)

_logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help", "--halp"]}


@click.group(
    invoke_without_command=True,
    context_settings=CONTEXT_SETTINGS,
)
@click.version_option(version=version.__version__)
@click.option("--debug", "-d", is_flag=True, help="Enable debug logging")
@click.pass_context
def embedops_cli(ctx, debug):
    """EmbedOps Base Command"""

    if debug:
        logging.basicConfig(level=logging.DEBUG)
        _logger.debug("Debug logging enabled")
    else:
        logging.basicConfig(level=logging.INFO)

    if ctx.invoked_subcommand is None:
        click.secho("-" * 80, fg="magenta")
        click.secho(
            "\n╭━━━╮╱╱╭╮╱╱╱╱╱╱╭┳━━━╮\n"
            "┃╭━━╯╱╱┃┃╱╱╱╱╱╱┃┃╭━╮┃\n"
            "┃╰━━┳╮╭┫╰━┳━━┳━╯┃┃╱┃┣━━┳━━╮\n"
            "┃╭━━┫╰╯┃╭╮┃┃━┫╭╮┃┃╱┃┃╭╮┃━━┫\n"
            "┃╰━━┫┃┃┃╰╯┃┃━┫╰╯┃╰━╯┃╰╯┣━━┃\n"
            "╰━━━┻┻┻┻━━┻━━┻━━┻━━━┫╭━┻━━╯\n"
            "╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃\n"
            "╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰╯\n",
            fg="magenta",
        )
        click.secho(
            "\nWelcome to EmbedOps CLI",
            err=False,
            fg="magenta",
        )
        click.secho("Version: " + version.__version__ + "\n")
        click.secho(
            "EmbedOps provides web-based and command-line tools that make setting\n"
            "up and maintaining your builds smooth and simple.\n\n"
            "EmbedOps tools also integrate directly with your automated CI\n"
            "pipelines, allowing any developer to run steps in their local dev\n"
            "environment exactly as it would be run on the CI server.\n"
        )
        click.secho(
            "Examples:\n"
            '"embedops-cli jobs show" provides a listing of the jobs that EmbedOps can run\n'
            '"embedops-cli jobs" enters an interactive mode for browsing your pipeline CI jobs\n'
            '"embedops-cli hil" enters an interactive mode for local HIL operations\n'
        )
        click.secho(
            "For a listing of all options, use embedops-cli --help, or embedops-cli -h\n"
        )
        click.secho("-" * 80, fg="magenta")
        click.secho("\n")


def _say_token_is_good(token_name: str):
    click.secho(f"\n{token_name} Token is ", nl=False)
    click.secho("GOOD", err=False, fg="bright_green")
    click.secho("You are logged into EmbedOps!\n", err=False, fg="white")


def _say_available_ci_jobs(job_list: list, wrong_job_name: str = None) -> None:
    user_jobs = [j for j in job_list if j not in ["release"]]
    if wrong_job_name:
        click.secho(
            f'\nJob "{wrong_job_name}" is not available in this CI configuration.\n',
            err=False,
            fg="yellow",
        )
    click.secho(
        f"EmbedOps CLI Jobs Available:",
        err=False,
        fg="magenta",
    )
    for j in user_jobs:
        click.secho(
            f" - {j}",
            err=False,
            fg="white",
        )


@embedops_cli.command()
@click.option("--test", "-t", help="Test your login status", is_flag=True)
def login(test):
    """Log in to the EmbedOps platform.
    You will be prompted to enter your EmbedOps credentials if you are not logged in."""

    docker_is_installed_and_running()

    token = embedops_authorization.get_auth_token()

    if token and embedops_authorization.check_token():
        _say_token_is_good("EmbedOps")
    elif test:
        click.secho("\nToken not found", err=False, fg="bright_red")
        click.secho(
            "\nuse `embedops-cli login` to log in and retrieve a token",
            err=False,
            fg="bright_red",
        )
        sys.exit(1)
    else:
        try:  # request a token if we don't already have one
            access_token = embedops_authorization.request_authorization()
            if access_token is None:
                raise LoginFailureException()
            embedops_authorization.set_auth_token(access_token)

        except (LoginFailureException, UnauthorizedUserException) as exc:
            echo_error_and_fix(exc)
            sys.exit(1)

    try:
        embedops_authorization.fetch_registry_token()
        embedops_authorization.login_to_registry()
    except (
        UnauthorizedUserException,
        LoginFailureException,
        DockerRegistryException,
        UnknownDockerException,
    ) as exc:
        echo_error_and_fix(
            exc
        )  # TODO: add context to these so we know WHICH login failed
    except DockerNotRunningException as exc:
        echo_error_and_fix(exc)
    else:
        _say_token_is_good("Docker")

    telemetry.login_event()


def print_command_info(ctx: click.Context, opts: click.STRING):
    """Helper function that echoes formatted CLI equivalent commands
    when user uses the wizard functionality."""
    click.secho(f"Equivalent command:\n", fg="magenta")
    click.secho(f"\t{ctx.command_path} {opts}\n", fg="white", color="white")


@embedops_cli.group(invoke_without_command=True)
@click.option(
    "--filename",
    help="path to the CI YAML or YML file",
    required=False,
    expose_value=True,
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
@click.pass_context
def jobs(ctx: click.Context, filename):
    """Run or view CI jobs defined in
    YAML or YML files locally.

    Try the interactive jobs runner available
    by running `embedops-cli jobs`."""

    if filename is None:
        try:
            filename = yaml_utilities.get_yaml_in_directory()
        except (NoYamlFileException, MultipleYamlFilesException) as exc:
            echo_error_and_fix(exc)

            click.secho(ctx.get_usage(), err=True, fg="white")
            sys.exit(2)
    else:
        if not (filename.lower().endswith(".yaml") or filename.endswith(".yml")):
            click.secho("-" * 80, fg="bright_red")
            click.secho("File must be a .yaml or .yml file.", err=True, fg="bright_red")
            click.secho(ctx.get_usage(), err=True, fg="white")
            click.secho("-" * 80, fg="bright_red")
            sys.exit(1)
    ctx.obj = filename

    _logger.debug(f"jobs show called with file {filename}")
    if not ctx.invoked_subcommand:
        click.secho("--- user controls " + "-" * 62, fg="magenta")
        click.secho("\t   navigation    : arrow keys (← → ↑ ↓)", fg="white")
        click.secho("\t   select        : enter key (↵)", fg="white")
        click.secho("\t   fuzzy search  : alphanumeric keys (a-zA-Z0-9)", fg="white")
        click.secho("")
        job_ctx_list = yaml_utilities.get_job_list(filename)
        job_name_list = [Choice(i.job_name) for i in job_ctx_list]

        job = inquirer.fuzzy(
            message="Select which job you would like to run",
            choices=job_name_list,
            multiselect=False,
            validate=lambda result: len(result) > 1,
        ).execute()

        action = inquirer.fuzzy(
            message=f"What would you like to do for job {job}?",
            choices=[
                Choice("run", name="Run Locally"),
                Choice("describe", name="Describe Job"),
                Choice(value=None, name="Cancel [cntl-c]"),
            ],
        ).execute()

        if not action:
            sys.exit(0)
        if "describe" == action:
            ctx.invoke(describe, job_name=job)
        elif "run" == action:
            ctx.invoke(run, job_name=job)
        print_command_info(ctx, f"--filename={filename} {action} {job}")


@jobs.command()
@click.pass_context
@click.argument("job_name")
@click.option(
    "--docker-cache/--no-docker-cache",
    help="Optionally disable the use of a local docker cache for EmbedOps Images",
    default=False,
    required=False,
    is_flag=True,
)
def run(ctx: click.Context, job_name, docker_cache=False):
    """Run a job defined in a CI YAML file.
    JOB_NAME is the name of the job or step in your CI YAML file"""

    telemetry.command_event("jobs_run", {"job_name": job_name})

    docker_is_installed_and_running()

    # check if token has expired if so try to get a new token
    if embedops_authorization.is_registery_token_valid() is False:
        embedops_authorization.login_to_registry()

    filename = ctx.obj
    _logger.debug(f"jobs run called with file '{filename}' and job '{job_name}")

    try:
        job = yaml_utilities.get_job(filename, job_name)
    except (
        UnsupportedYamlTypeException,
        BadYamlFileException,
    ) as exc:
        echo_error_and_fix(exc)
        ctx.exit(2)

    # match the given job name against the job collection
    if job:
        git_hash_run = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
        )
        if git_hash_run.returncode != 0:
            git_hash = "Not Available"
        else:
            git_hash = git_hash_run.stdout.strip()
        repo_id = get_repo_id() or "N/A"
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        click.secho("-" * 80, fg="magenta")
        click.secho(f"Running job   '{job_name}'", err=False, fg="magenta")
        click.secho(f"-> repo id    '{repo_id}'", err=False, fg="white")
        click.secho(f"-> file       '{filename}'", err=False, fg="white")
        click.secho(f"-> directory  '{os.getcwd()}'", err=False, fg="white")
        click.secho(
            f"-> image      '{job.docker_tag if job.docker_tag else 'N/A'}'",
            err=False,
            fg="white",
        )
        click.secho(f"-> git sha    '{git_hash}'", err=False, fg="white")
        click.secho(f"-> timestamp  '{current_time}'", err=False, fg="white")
        click.secho("-" * 80, fg="magenta")
        click.secho("\n")
        try:
            run_exitcode = docker_run.docker_run(job, docker_cache)
        except (
            EmbedOpsException,
            NoDockerContainerException,
            InvalidDockerContainerException,
        ) as exc:
            echo_error_and_fix(exc)
            ctx.exit(1)
        if run_exitcode == 0:
            click.secho("\nJob ran successfully\n", err=False, fg="magenta")
        else:
            click.secho("\nJob ran with errors\n", err=True, fg="red")
    # They tried to run a job that doesn't exist, show them the jobs they can run.
    else:
        try:
            _say_available_ci_jobs(_get_job_name_list(filename), job_name)
        except (UnsupportedYamlTypeException, BadYamlFileException) as exc:
            echo_error_and_fix(exc)
            ctx.exit(2)


@jobs.command()
@click.option(
    "-v",
    "--verbose",
    help="Show details for the available jobs in YAML file",
    required=False,
    expose_value=True,
    is_flag=True,  # Inform Click that this is a boolean flag
)
@click.pass_context
def show(ctx: click.Context, verbose):
    """Show available jobs in YAML file"""

    telemetry.command_event("jobs_show", {"verbose": verbose})

    filename = ctx.obj
    _logger.debug(f"jobs show called with file {filename}")

    if not verbose:
        try:
            job_list = _get_job_name_list(filename)
            job_name_list = "\n".join([i for i in job_list if not i == "release"])
        except (UnsupportedYamlTypeException, BadYamlFileException) as exc:
            echo_error_and_fix(exc)
            ctx.exit(2)

        click.secho(f"\nEmbedOps CLI Jobs Available:", err=False, fg="magenta")
        click.secho(f"{job_name_list}\n", err=False, fg="white")
    else:
        try:
            job_list = yaml_utilities.get_job_list(filename)
        except (
            UnsupportedYamlTypeException,
            BadYamlFileException,
        ) as exc:
            echo_error_and_fix(exc)
            ctx.exit(2)

        click.secho("\nEmbedOps CLI Jobs Details:\n", err=False, fg="magenta")

        # match the given job name against the job collection
        for job in job_list:
            click.secho(job.pretty())


@jobs.command()
@click.pass_context
@click.argument("job_name")
def describe(ctx: click.Context, job_name):
    """Shows details for a single job"""

    telemetry.command_event("jobs_describe", {"job_name": job_name})

    filename = ctx.obj
    _logger.debug(f"jobs describe called with file {filename}")

    try:
        job = yaml_utilities.get_job(filename, job_name)
    except (
        UnsupportedYamlTypeException,
        BadYamlFileException,
    ) as exc:
        echo_error_and_fix(exc)
        ctx.exit(2)

    # match the given job name against the job collection
    if job is not None:
        click.secho(job.pretty())
    # They tried to show details of a job that doesn't exist, show them the jobs they can run.
    else:
        try:
            _say_available_ci_jobs(_get_job_name_list(filename), job_name)
        except (UnsupportedYamlTypeException, BadYamlFileException) as exc:
            echo_error_and_fix(exc)
            ctx.exit(2)


# Handle the 'hil' command group
@embedops_cli.group(invoke_without_command=True)
@click.option(
    "--devices",
    help='Comma delimited list of device names to run hil "blink" and "run" command on',
    required=False,
    expose_value=True,
    callback=lambda ctx, value: value.split(",") if value else None,
)
@click.pass_context
def hil(ctx, devices):
    """Group for all hil commands.

    Try the interactive HIL runner available
    by running `embedops-cli hil`."""
    ctx.ensure_object(dict)
    ctx.obj["devices"] = devices

    if not ctx.invoked_subcommand:
        click.secho("--- user controls " + "-" * 62, fg="magenta")
        click.secho("\t   navigation    : arrow keys (← → ↑ ↓)", fg="white")
        click.secho("\t   select/accept : enter key (↵)", fg="white")
        click.secho("\t   multiselect   : tab key (⇥)", fg="white")
        click.secho("\t   fuzzy search  : alphanumeric keys (a-zA-Z0-9)", fg="white")
        click.secho("")
        repo_fleet_devices = hil_commands.get_repo_fleet_devices()
        choices = [
            Choice("run", name="Run Locally"),
            Choice("blink", name="Blink Gateway"),
            Choice(value=None, name="Cancel [cntl-c]"),
        ]
        if len(repo_fleet_devices) < 6:
            choices.insert(-1, Choice("provision", name="Provision New Gateway"))
        else:
            click.secho(
                "At account maximum, unable to provision new HIL gateways", fg="yellow"
            )

        action = inquirer.fuzzy(
            message="What HIL operation would you like to do?",
            choices=choices,
        ).execute()

        if not action:
            sys.exit(0)

        if "provision" == action:
            print_command_info(ctx, f"{action}")
            # invoke provision command
            ctx.invoke(getattr(hil_commands, action))
        else:
            if len(repo_fleet_devices) >= 1:
                choices = [
                    Choice(
                        d.device_name,
                        name=f"{d.device_name} ({'Online' if d.is_online else 'Offline'})",
                    )
                    for d in repo_fleet_devices
                ]
                if "run" == action:
                    choices.insert(0, Choice("any", name="Any"))
                elif "blink" == action:
                    pass
                devices = inquirer.fuzzy(
                    message=f"Select a HIL gateway to {action}",
                    choices=choices,
                    multiselect=True,
                    validate=lambda result: len(result) >= 1,
                ).execute()

                if "any" not in devices:
                    ctx.obj["devices"] = devices
                    print_command_info(ctx, f"--devices {','.join(devices)} {action}")
                else:
                    print_command_info(ctx, f"{action}")
                # invoke run/blink command
                ctx.invoke(getattr(hil_commands, action))
            else:
                click.secho("no devices provided or none in fleet")


# Add sub-commands to the hil group
hil.add_command(hil_commands.blink)
hil.add_command(hil_commands.run)
hil.add_command(hil_commands.fleet)
hil.add_command(hil_commands.provision)


def _get_job_name_list(_filename: str) -> list:
    try:
        parser = yaml_utilities.get_correct_parser_type(_filename)
    except UnsupportedYamlTypeException as exc:
        raise UnsupportedYamlTypeException() from exc

    try:
        return parser.get_job_name_list(_filename)
    except BadYamlFileException as exc:
        raise BadYamlFileException() from exc


def docker_is_installed_and_running():
    """Check if docker is installed and running"""
    try:
        try:
            subprocess.check_output(
                ("powershell " if platform.system() == "Windows" else "")
                + "docker info",
                shell=True,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError as err:
            if err.returncode == 127:
                raise NoDockerCLIException from err
            if "Is the docker daemon running?" in str(err.stdout):
                raise DockerNotRunningException from err
            raise UnknownDockerException from err
    except (
        NoDockerCLIException,
        DockerNotRunningException,
        UnknownDockerException,
    ) as err:
        echo_error_and_fix(err)
        sys.exit(1)


if __name__ == "__main__":
    embedops_cli(prog_name="embedops-cli")  # pylint:disable=unexpected-keyword-arg
