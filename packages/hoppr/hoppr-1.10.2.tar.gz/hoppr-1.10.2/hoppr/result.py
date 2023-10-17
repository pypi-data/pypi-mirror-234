"""
Class to store results of processes
"""
from __future__ import annotations

from enum import IntEnum
from typing import Any

import requests

from hoppr.exceptions import HopprError


class ResultStatus(IntEnum):
    """
    Enumeration of possible result states
    """

    EXCLUDED = 0
    SUCCESS = 1
    RETRY = 2
    FAIL = 3
    SKIP = 4


class Result:
    """
    Class to store results of processes
    """

    def __init__(self, status: ResultStatus, message: str = "", return_obj: Any = None):
        self.status = status
        self.message = message
        self.return_obj = return_obj

    def __str__(self):
        result_msg = f"{self.status.name}"
        if self.message != "":
            result_msg += f", msg: {self.message}"

        return result_msg.rstrip()

    @staticmethod
    def success(message="", return_obj: Any = None) -> Result:
        """
        Convenience method for generating success messages
        """
        return Result(ResultStatus.SUCCESS, message, return_obj)

    @staticmethod
    def retry(message="", return_obj: Any = None) -> Result:
        """
        Convenience method for generating retry messages
        """
        return Result(ResultStatus.RETRY, message, return_obj)

    @staticmethod
    def fail(message="", return_obj: Any = None) -> Result:
        """
        Convenience method for generating failure messages
        """
        return Result(ResultStatus.FAIL, message, return_obj)

    @staticmethod
    def excluded(message="", return_obj: Any = None) -> Result:
        """
        Convenience method for generating excluded messages
        """
        return Result(ResultStatus.EXCLUDED, message, return_obj)

    @staticmethod
    def skip(message="", return_obj: Any = None) -> Result:
        """
        Convenience method for generating skip messages
        """
        return Result(ResultStatus.SKIP, message, return_obj)

    def is_success(self) -> bool:
        """
        Convenience method for testing for success messages
        """
        return self.status == ResultStatus.SUCCESS

    def is_retry(self) -> bool:
        """
        Convenience method for testing for retry messages
        """
        return self.status == ResultStatus.RETRY

    def is_fail(self) -> bool:
        """
        Convenience method for testing for failure messages
        """
        return self.status == ResultStatus.FAIL

    def is_excluded(self) -> bool:
        """
        Convenience method for testing for excluded messages
        """
        return self.status == ResultStatus.EXCLUDED

    def is_skip(self) -> bool:
        """
        Convenience method for testing for skip messages
        """
        return self.status == ResultStatus.SKIP

    def merge(self, other: Result):
        """
        Logically combine two Result objects
        """
        if other.is_skip():
            return

        self.status = max(self.status, other.status)
        if self.message == "":
            self.message = other.message
        else:
            self.message += "\n" + other.message

        if self.return_obj is None:
            self.return_obj = other.return_obj
        elif other.return_obj is not None:
            raise HopprError("Unable to merge two results with return objects")

        return

    @staticmethod
    def from_http_response(response: requests.Response, return_obj: Any = None):
        """
        Build a Result object from an HTTP request response
        """

        match response.status_code:
            case response_code if 200 <= response_code <= 299:
                return Result.success(
                    f"HTTP Status Code: {response.status_code}",
                    return_obj=return_obj,
                )
            case response_code if response_code >= 500:
                status = ResultStatus.RETRY
            case _:
                status = ResultStatus.FAIL

        message = f"HTTP Status Code: {response.status_code}; {response.reason or response.text}"
        return Result(status, message, return_obj=return_obj)
