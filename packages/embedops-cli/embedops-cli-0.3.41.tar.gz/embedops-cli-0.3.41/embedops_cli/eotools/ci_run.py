#!/usr/bin/env python
"""
`ci_run.py`
=======================================================================
A small script to create and update EmbedOps CI run records
* Author(s): Bryan Siepert
"""
import sys
import time
import importlib
import logging
from os import getenv
from urllib3.exceptions import ReadTimeoutError
from embedops_cli.api import (
    Configuration,
    CIRunCreateProps,
    CIRunUpdateProps,
    rest,
)
from embedops_cli.utilities import get_client
import embedops_cli.config

_logger = logging.getLogger("create_run")


class CiConfigs:
    """Class representing configurations set by CI"""

    def __init__(  # pylint: disable=R0913
        self,
        commit_id,
        branch_name,
        source_type,
        pipeline_id=None,
        pipeline_url=None,
    ):
        self.commit_id = commit_id
        self.branch_name = branch_name
        self.source_type = source_type
        self.pipeline_id = pipeline_id
        self.pipeline_url = pipeline_url


class CIRun:
    """A wrapper for creating and updating CIRun records"""

    def __init__(self):
        # pylint: disable=import-outside-toplevel

        importlib.reload(embedops_cli.config)
        self._settings = embedops_cli.config.settings

    # create().id
    def create_main(self):
        """The main entrypoint for the module, to allow for binary-izing"""

        env_error = False
        http_timeout = None
        max_retries = None

        if getenv("CI") is None or getenv("CI") != "true":
            _logger.info("LOCAL")
            sys.exit(0)

        if self._settings.get("commit") is None:
            _logger.error("ERROR: No commit id envvar found")
            env_error = True

        if self._settings.get("branch") is None and self._settings.get("tag") is None:
            _logger.error("ERROR: No branch or tag name envvar found")
            env_error = True

        if self._settings.get("analysis_type") is None:
            _logger.error("ERROR: No analysis type envvar found")
            env_error = True

        if self._settings.get("api_repo_key") is None:
            _logger.error("ERROR: No EMBEDOPS_API_REPO_KEY envvar found")
            env_error = True

        http_timeout = int(self._settings.get("http_timeout", 60))
        max_retries = int(self._settings.get("max_retries", 5))

        if env_error is True:
            sys.exit(1)

        analysis_type = self._settings.analysis_type
        commit_id = self._settings.commit
        branch_name = (
            self._settings.tag
            if self._settings.get("branch") is None
            else self._settings.branch
        )
        source_type = self._settings.get("source_type")
        pipeline_id = self._settings.get("pipeline_id")
        job_name = self._settings.get("job_name")
        pipeline_url = self._settings.get("job_url")

        return self.create(
            analysis_type,
            CiConfigs(commit_id, branch_name, source_type, pipeline_id, pipeline_url),
            http_timeout,
            max_retries,
            job_name,
        )

    @staticmethod
    def create(
        analysis_type,
        ci_configs,
        timeout,
        max_retries,
        job_name=None,
    ):

        """Use the branch name, commit sha, analysis type, job_name,
        and pipeline id to create a new ciRun instance"""

        # implement retries manually since urllib3 version is locked in place
        response = None
        for retry in range(0, int(max_retries) + 1):
            api_client = get_client()
            try:
                create_properties = CIRunCreateProps(
                    branch=ci_configs.branch_name,
                    source_type=ci_configs.source_type,
                    commit_id=ci_configs.commit_id,
                    type=analysis_type,
                    pipeline_id=ci_configs.pipeline_id,
                    name=job_name,
                    pipeline_url=ci_configs.pipeline_url,
                )
                response = api_client.create_ci_run_from_ci(
                    create_properties, _request_timeout=timeout
                )
                break

            except (ValueError, TypeError, rest.ApiException, ReadTimeoutError) as err:
                if retry >= int(max_retries):
                    _logger.warning(f"max retries ({max_retries}) reached, aborting")
                    sys.exit(1)
                else:
                    _logger.error(f"retry: {retry} out of {max_retries}")
                if len(err.args) > 0:
                    _logger.error(err.args[0])
                else:
                    _logger.error(err)
                    if err.status >= 500:
                        # "Service Temporarily Unavailable"
                        # server is likely down for a brief maintenance window
                        _logger.warning(
                            f"[{err.status}] {err.reason}), delaying {timeout} seconds before retry"
                        )
                        time.sleep(timeout)
            finally:
                # this kills the thread pool so the process can exit
                del api_client
        return response

    def _update_ci_run(self, status_str):

        try:
            api_client = get_client()
            configuration = Configuration()
            configuration.api_key["X-API-Key"] = self._settings.api_repo_key
            configuration.host = f"{self._settings.host}/api/v1"

            ci_run = CIRunUpdateProps()
            ci_run.status = status_str
            updated_run = api_client.update_ci_run_from_ci(
                ci_run, self._settings.run_id
            )

            _logger.debug("Updated CI run:")
            _logger.debug(updated_run)

            del api_client  # kills the thread pool
        except AttributeError as exc:
            _logger.info("No API Repo Key provided. CI run will not be updated.")
            _logger.info(exc)

    @staticmethod
    def _previous_return():
        return int(sys.argv[1])

    def finalize_ci_run(self):
        """Update the status of the current CI run based on the value of a standard in read"""
        previous_return = self._previous_return()
        if previous_return != 0:
            self._update_ci_run("failure")
        else:
            self._update_ci_run("success")


def update_entry():
    """Entrypoint for the `eotools-update-run` tool"""
    ci_run = CIRun()
    ci_run.finalize_ci_run()


def create_entry():
    """Entrypoint for the `eotools-create-run` tool"""
    ci_run = CIRun()
    new_ci_run = ci_run.create_main()
    _logger.info(new_ci_run.id)
    # DO NOT REMOVE. need to output ID for eotools-create-run
    print(new_ci_run.id)
    sys.exit(0)


if __name__ == "__main__":
    create_entry()
