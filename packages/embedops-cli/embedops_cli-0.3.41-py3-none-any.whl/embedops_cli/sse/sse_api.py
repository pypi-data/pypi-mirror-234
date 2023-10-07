"""
SSEApi contains a class to interface to the Embedops Server's SSE endpoints, and process the events.
"""

import json
import urllib3
import sseclient
from embedops_cli import embedops_authorization
from embedops_cli.config import settings
from embedops_cli.eo_types import NetworkException, UnauthorizedUserException


class SSEApi:

    """SSEApi functions similarly to the default HTTP API object except
    it is limited to SSE endpoints only"""

    def __init__(self):
        """Get an SEE client for the embedops SSE API as the currently signed in user"""

        api_host = settings.get("host")
        self.api_prefix = f"{api_host}/api/v1"

    def sse_blink_gateway(self, repo_id, devices=None):
        """Blink the gateway. Returns events from the event stream."""
        request_body = (
            json.dumps({"deviceNames": devices}) if devices is not None else None
        )

        for event in self._sse_perform_request(
            f"/repos/{repo_id}/hil/blink", request_body
        ):
            yield event

    def sse_hil_run(self, repo_id, devices=None):
        """Perform local HIL run. Returns events from the event stream."""

        request_body = (
            json.dumps({"deviceNames": devices}) if devices is not None else None
        )

        for event in self._sse_perform_request(
            f"/repos/{repo_id}/hil/test-runs", request_body
        ):
            yield event

    def _sse_perform_request(self, endpoint: str, request_body=None) -> int:
        """
        Perform an SSE request via HTTP, yielding events as they are generated.
        This function should be used in a for loop to receive events as they are generated
        """

        # Retrieve auth token from settings
        auth_token = embedops_authorization.get_auth_token()
        if auth_token is None:
            raise UnauthorizedUserException()

        http = urllib3.PoolManager()
        headers = {
            "Accept": "text/event-stream",
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }
        full_url = self.api_prefix + endpoint
        response = http.request(
            "POST",
            full_url,
            preload_content=False,
            headers=headers,
            body=request_body,
        )

        if response.status != 200:
            raise NetworkException(response.status)

        client = sseclient.SSEClient(response)
        for event in client.events():
            yield event
