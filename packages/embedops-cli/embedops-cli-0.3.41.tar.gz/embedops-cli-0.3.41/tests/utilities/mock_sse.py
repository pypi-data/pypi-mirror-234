"""
This module mocks out an SSE response, as requested by urllib3.
"""
import json

AUTH_TOKEN_GOOD = 'AUTH_TOKEN_GOOD'
AUTH_TOKEN_BAD = 'AUTH_TOKEN_BAD'

mock_events = []


class MockEventResponse(object):

    """Represents a mock response object that will be returned by the mock request handler.
    This class effectively emulates a """

    def __init__(self, status, events):

        self.status = status
        self.events = events
        self.event_index = 0

    def raise_for_status(self):
        pass

    def __iter__(self):
        return self

    def __next__(self, chunk_size=1024):

        if self.event_index == len(self.events):
            raise StopIteration

        event = self.events[self.event_index]
        event_str = "event: %s\ndata: %s\n\n" % (event["event"], event["data"])
        self.event_index += 1
        return event_str.encode()


def mock_sse_request_handler(method, url, fields=None, headers=None, **urlopen_kw):

    """A mock function for the urllib3 PoolManager.request function. Has the same parameters,
    but returns a mock response object instead. This function will return 401 if the provided
    token in the header is not AUTH_TOKEN_GOOD"""

    # Check for authorization
    if headers["Authorization"] != ('Bearer ' + AUTH_TOKEN_GOOD):
        return MockEventResponse(401, [])

    response = MockEventResponse(200, mock_events)

    return response


def set_mock_events(events):

    global mock_events
    mock_events = events
