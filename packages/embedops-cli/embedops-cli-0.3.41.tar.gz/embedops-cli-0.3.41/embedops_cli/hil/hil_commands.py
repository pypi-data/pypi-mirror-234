"""
Contains functions for the HIL sub-group commands.
"""
import os
import json
import traceback
import click
import requests
from embedops_cli.eo_types import (
    NoRepoIdException,
    NetworkException,
    LoginFailureException,
    UnauthorizedUserException,
)
from embedops_cli.api.rest import ApiException
from embedops_cli.hil.hil_types import (
    HILRepoId404Exception,
    HILImageConfigException,
)
from embedops_cli.sse.sse_api import SSEApi
from embedops_cli.sse import eo_sse
from embedops_cli.utilities import echo_error_and_fix
from embedops_cli import config
from embedops_cli.hil.hil_common import HIL_GATEWAY_IMAGE_NAME
from embedops_cli.hil.image_utility import write_image_config
from embedops_cli.hil.hil_common import hil_run
from embedops_cli import embedops_authorization


@click.command()
@click.pass_context
def blink(ctx: click.Context):
    """Get a streaming response for the given event feed using urllib3."""
    try:
        repo_id = config.get_repo_id()

        if not repo_id:
            raise NoRepoIdException()

        sse_api = SSEApi()
        for event in sse_api.sse_blink_gateway(repo_id, ctx.obj["devices"]):
            if event.event == eo_sse.SSE_TEXT_EVENT:
                eo_sse.sse_print_command_text(event)
            elif event.event == eo_sse.SSE_RESULT_EVENT:
                result_event_obj = json.loads(event.data)
                ctx.exit(result_event_obj["exitCode"])
            else:
                pass  # Just ignore

        # If the command hasn't returned anything yet, exit here
        ctx.exit(2)

    except NoRepoIdException as exc:
        echo_error_and_fix(exc)
        ctx.exit(2)
    except NetworkException as exc:
        if exc.status_code == 401:
            echo_error_and_fix(LoginFailureException())
        elif exc.status_code == 404:
            echo_error_and_fix(HILRepoId404Exception())
        else:
            echo_error_and_fix(exc)

        ctx.exit(2)


@click.command()
@click.pass_context
def run(ctx: click.Context):
    """Run hil in local mode, using the current repository as a source."""

    ctx.exit(hil_run(local=True, devices=ctx.obj["devices"]))


def get_repo_fleet_devices():
    """Helper function that simplifies retrieving
    list of devices in fleet.

    Raises:
        NoRepoIdException: _description_

    Returns:
        list(dict()): list of device dictionaries
                      containing device id, name
                      and online status
    """
    repo_id = config.get_repo_id()

    if not repo_id:
        raise NoRepoIdException()

    api_client = embedops_authorization.get_user_client()
    return api_client.get_repo_fleet_devices(repo_id)


@click.command()
@click.pass_context
def fleet(ctx: click.Context):
    """Get a list of fleet devices for the current repo."""

    try:
        fleet_devices = get_repo_fleet_devices()

        if len(fleet_devices) == 0:
            click.echo("No devices found in fleet.")
            return

        max_name_length = max(len(device.device_name) for device in fleet_devices)

        for device in fleet_devices:
            if device.is_online:
                status = click.style("Online", fg="green")
            else:
                status = click.style("Offline", fg="red")

            click.echo(f"{device.device_name.ljust(max_name_length)}\t{status}")

    except NoRepoIdException as exc:
        echo_error_and_fix(exc)
        ctx.exit(2)
    except ApiException as exc:
        if exc.status == 401:
            echo_error_and_fix(LoginFailureException())
        elif exc.status == 404:
            echo_error_and_fix(HILRepoId404Exception())
        else:
            echo_error_and_fix(NetworkException(exc.status))

        ctx.exit(2)
    except Exception as exc:  # pylint: disable=broad-except
        traceback.print_exc()
        ctx.exit(2)


@click.command()
@click.pass_context
def provision(ctx: click.Context):
    """Provision a new device by creating a new OS image that can
    be flashed with an external utility. The new image
    is created in the current directory, named gateway-image.img."""

    try:
        repo_id = config.get_repo_id()
        if not repo_id:
            raise NoRepoIdException()

        api_client = embedops_authorization.get_user_client()

        url_data = api_client.get_latest_gateway_image_url()
        latest_image_url = url_data.url

        try:
            os.remove(HIL_GATEWAY_IMAGE_NAME)
        except FileNotFoundError:
            pass

        click.secho("Downloading latest gateway image...")
        with open(HIL_GATEWAY_IMAGE_NAME, "wb") as out_file:
            download_response = requests.get(latest_image_url, stream=True, timeout=300)

            if not download_response.ok:
                raise ApiException(download_response.status_code)

            out_file.write(download_response.content)

        click.secho("Provisioning device...")

        provision_data = api_client.hil_provision_device(repo_id)

        device_config_string = provision_data.device_config

        if not write_image_config(HIL_GATEWAY_IMAGE_NAME, device_config_string):
            raise HILImageConfigException()

        click.secho(
            f"{provision_data.device_name} has been provisioned. "
            f"Please complete provisioning by flashing {HIL_GATEWAY_IMAGE_NAME}"
            f" to an SD card. We recommend using either Balena Etcher"
            f" (https://github.com/balena-io/etcher)"
            f" or Raspberry Pi Imager"
            f" (https://github.com/raspberrypi/rpi-imager).\n"
        )

    except (
        NoRepoIdException,
        NetworkException,
        UnauthorizedUserException,
        HILImageConfigException,
    ) as exc:
        echo_error_and_fix(exc)
        ctx.exit(2)
    except ApiException as exc:
        echo_error_and_fix(NetworkException(exc.status))
        ctx.exit(2)
