#!/usr/bin/env python
"""
`parse.py`
=======================================================================
A script to parse information from build logs
* Author(s): Bryan Siepert
"""
import os
import re
import json
from sys import exit as sys_exit
from pprint import pformat
import click
from embedops_cli.config import settings
from embedops_cli.utilities import logging_setup
from embedops_cli.utilities import post_dict, get_compiler
from embedops_cli.eotools.iar_parser.ewp import (
    get_configuration_mapfile_path,
    IARNoListOptionException,
    IARNoIlinkOutputFileOptionException,
    IARProjectSettingsNotFoundException,
    IAREwpFileNotFoundException,
    IARMapFileNotFoundException,
)
from embedops_cli.eotools.iar_parser.iar import (
    SIZE_PATTERN as IAR_SIZE_PATTERN,
    pack_result as iar_pack_result,
    IARNoMemoryMetricsFoundInMapFileException,
)
from embedops_cli.eotools.log_parser.gnu_size_berkeley import (
    SIZE_PATTERN as SIZE_SIZE_PATTERN,
    pack_result as gnu_pack_result,
)

_logger = logging_setup(__name__)
EXPECTED_RETURN_CODE = 200


def parse_storage_sizes(
    log_filename, compiler, iar_config=None
):  # pylint: disable=R0914
    """Check each line in a log file for compiler RAM, flash data, and flash code sizes"""

    build_data = None
    storage_sizes = None
    storage_collection = []

    if compiler == "IAR":
        size_regex = IAR_SIZE_PATTERN
        _logger.info("IAR size pattern loaded")
        _logger.info(
            f"Parsing IAR configuration '{iar_config}' from project (.ewp) file: {log_filename}"
        )
        try:
            map_path = get_configuration_mapfile_path(log_filename, iar_config)
        except (
            IARNoListOptionException,
            IARNoIlinkOutputFileOptionException,
            IARProjectSettingsNotFoundException,
            IAREwpFileNotFoundException,
            IARMapFileNotFoundException,
        ) as exc:
            click.secho(f"Unable to parse storage sizes: {exc.message}", fg="red")
            sys_exit(1)

        _logger.debug(f"path to map file: {map_path}")
        mapfile_name = os.path.basename(map_path).replace(".map", "")
        with open(map_path, "r", encoding="ascii") as map_file:
            build_data = map_file.read()
        regex_result = re.finditer(size_regex, build_data)
        if regex_result:
            build_result = iar_pack_result(
                next(regex_result).groupdict(), mapfile_name, iar_config
            )
            _logger.debug(f"build result: {build_result}")
        else:
            raise IARNoMemoryMetricsFoundInMapFileException(
                message=f"Unable to parse memory metrics from '{iar_config}' in {map_path}"
            )
        _logger.debug(f"final build result: {build_result}")
        storage_collection.append(build_result)
    else:
        if compiler in ("TI", "GCC"):
            size_regex = SIZE_SIZE_PATTERN
            _logger.info("GNU size pattern loaded for TI and GCC")
        else:
            _logger.warning(f"EMBEDOPS_COMPILER {compiler} not supported")
            sys_exit(1)

        if os.path.exists(log_filename):
            with open(log_filename, "r", encoding="ascii") as build_log:
                build_data = build_log.read()
        else:
            _logger.critical(f"log file {log_filename} not found")
            sys_exit(1)

        build_results = re.finditer(size_regex, build_data)
        for result in build_results:
            storage_sizes = gnu_pack_result(result)
            _logger.debug(f"build result: {storage_sizes}")
            storage_collection.append(storage_sizes)
    _logger.debug(f"parsed metrics: {json.dumps(storage_collection, indent=2)}")
    return storage_collection


def _report_metrics(metrics_collections, run_id, embedops_repo_key):

    headers = {"X-API-Key": embedops_repo_key, "Content-Type": "application/json"}
    if run_id == "LOCAL":
        _logger.info("\nResults:")

    for build_metrics in metrics_collections:
        for key in build_metrics:
            if key == "dimensions":
                continue
            stats_data = {
                "ciRunId": run_id,
                "name": key,
                "value": build_metrics[key],
                "dimensions": build_metrics["dimensions"],
            }

            if run_id == "LOCAL":
                _logger.info(f"\t{key} : {pformat(build_metrics[key])}")
            else:
                response = post_dict(
                    settings.metrics_endpoint,
                    json_dict=stats_data,
                    headers=headers,
                )
                # TODO: Refactor this to remove the duplication with similar
                # code in `create_run.py`, perhaps in a shared API library :O
                if response.status_code != EXPECTED_RETURN_CODE:
                    _logger.error(
                        f"FAILING: Expected response type {EXPECTED_RETURN_CODE}(Created)"
                        f"from metrics creation endpoint, got {response.status_code}"
                    )
                    response_string = pformat(response.json(), indent=4)
                    _logger.error(response_string)

                    sys_exit(1)
                response_string = pformat(response.json(), indent=4)
                _logger.info("Created metric:")
                _logger.info(response_string)


def parse_reports(input_filename, compiler, run_id, embedops_repo_key, iar_config=None):
    """Parse the given file for compile sized totals"""
    if not os.path.exists(input_filename):
        click.secho(
            f"Unable to parse storage sizes: {input_filename} does not exist", fg="red"
        )
        sys_exit(1)
    storage_sizes = parse_storage_sizes(input_filename, compiler, iar_config=iar_config)
    _logger.info(f"Got storage sizes: {json.dumps(storage_sizes, indent=2)}")
    if not storage_sizes:
        click.secho("no build target sizes found", fg="red")
    _report_metrics(storage_sizes, run_id, embedops_repo_key)


@click.group(
    invoke_without_command=True,
)
@click.option("--debug", "-d", help="enable debugging", is_flag=True)
@click.option(
    "--iar-ewp-file", help="path to iar .ewp project file for memory metrics parsing"
)
@click.option(
    "--iar-config", help="the IAR project configuration (e.g. Debug, Production)"
)
def main(iar_ewp_file: str = None, iar_config: str = None, debug: bool = False):
    """The main entrypoint for the module
    If provided, the IAR project file is used instead of the build log file. This is
    used to find the .map file for memory metrics parsing.
    """

    if debug:
        global _logger  # pylint: disable=W0603
        _logger = logging_setup(__name__, "DEBUG")
        _logger.setLevel("DEBUG")
        _logger.debug(f"EWP File: {iar_ewp_file}")
        _logger.debug(f"IAR Config: {iar_config}")

    compiler = get_compiler()
    if compiler not in ("IAR", "TI", "GCC"):
        click.secho("EMBEDOPS_COMPILER not set", fg="red")
        sys_exit(1)
    input_file = iar_ewp_file or settings.input_file
    run_id = settings.run_id

    try:
        api_repo_key = settings.api_repo_key
    except AttributeError:
        api_repo_key = None

    _logger.info(f"EMBEDOPS_INPUT_FILE {input_file}")
    _logger.info(f"EMBEDOPS_RUN_ID {run_id}")

    if run_id is None:
        _logger.warning(
            "EMBEDOPS_RUN_ID not set. Assuming local build, will not push metrics"
        )
        run_id = "LOCAL"
    elif run_id == "LOCAL":
        _logger.info("Local build requested. Will not push metrics")
    elif api_repo_key is None:
        _logger.warning(
            "EMBEDOPS_API_REPO_KEY not set. Assuming local build, will not push metrics."
        )
        run_id = "LOCAL"

    _logger.info("EMBEDOPS_API_REPO_KEY set (not echoing)")

    # this should read directly from settings
    parse_reports(input_file, compiler, run_id, api_repo_key, iar_config=iar_config)
