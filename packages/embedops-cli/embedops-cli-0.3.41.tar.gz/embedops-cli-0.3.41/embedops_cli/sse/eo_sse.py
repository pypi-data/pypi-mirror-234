"""
Contains the Embedops CLI specific SSE definitions
and the actions we take upon receiving them
"""

import json
import click

# Event types
SSE_TEXT_EVENT = "CLIEventCommandText"
SSE_RESULT_EVENT = "CLIEventCommandResult"

# Colors for log levels
LOG_LEVEL_COLOR_MAP = {"info": "white", "warning": "yellow", "error": "bright_red"}


def sse_print_command_text(event):

    """Print the text from SSE_TEXT_EVENT"""

    text_event_obj = json.loads(event.data)
    error = text_event_obj["logLevel"] == "error"
    click.secho(
        text_event_obj["displayText"],
        err=error,
        fg=LOG_LEVEL_COLOR_MAP[text_event_obj["logLevel"]],
    )
