# TODO better docs, dynamic message to identify engine
import json

from h2o_engine_manager.gen.dai_engine_service import ApiException as GenApiException


class FailedEngineException(Exception):
    """Exception raised for STATE_FAILED while waiting for engine update."""

    def __init__(self):
        super().__init__("Engine has FAILED")


class TimeoutException(Exception):
    """Exception raised when timeout is exceeded."""

    def __init__(self):
        super().__init__("Timeout exceeded")


class ApiException(GenApiException):
    """ApiException with simplified error message.

    Beware, it can be used also for h2o_engine_manager.gen.dai_version_service or 'any other' ApiException
    (because python doesn't care which data type is on the input as long as it has the class has the same-named fields).
    """

    def __init__(self, e: GenApiException):
        self.status = e.status
        self.reason = e.reason
        self.body = e.body
        self.headers = e.headers

    def __str__(self):
        status_reason = f"{self.status} ({self.reason})"
        message = self.body

        if message is None:
            return status_reason

        try:
            body_json = json.loads(self.body)
            message = body_json["message"]
        except (ValueError, KeyError):
            pass

        return f"{status_reason}: {message}"
