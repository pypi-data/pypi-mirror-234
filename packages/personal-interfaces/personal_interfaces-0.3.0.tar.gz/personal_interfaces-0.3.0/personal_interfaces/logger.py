"""
Logger for the server
"""
import os
from functools import partial
from typing import Callable, Dict
from datetime import datetime
import attr
from rich.console import Console
# "Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i]."


@attr.s(slots=True)
class Logger:  # pylint: disable=R0903
    """Logger object for the server"""
    _console: Console = attr.ib(default=Console())
    _url: str = attr.ib(default=None)
    _date: Callable = attr.ib(default=None)
    _log: Dict[str, Callable] = attr.ib(default=None)
    _instances: dict = {}

    def __new__(cls, *args, **kwargs) -> None:
        """Custom call to create a singleton instance"""
        # Search for the class in the instances
        if cls not in cls._instances:
            # If this class doesn't exist, create a new one}
            instance = super(Logger, cls).__new__(cls, *args, **kwargs)
            cls._instances[cls] = instance
        # Return the instances created and stored in the instances dict
        return cls._instances[cls]

    def __attrs_post_init__(self):
        # Create a lambda function to obtain the time at each iteration that we call the logger
        self._date = datetime.now
        # Initialize the url as a localhost in case that we don't provide one
        self._url = os.environ.get('URL', "")
        # Initialize the status dict
        self.__status()

    def __status(self) -> None:
        """Private method to define the status for the logger."""
        # Define the lambda to be called in the dict
        def _print(color: str, status: str, msg: str, endpoint: str = "") -> None:
            self._console.print(
                f"[bold {color}]" +
                f"-[S:{status}|D:{self._date()}" +
                f"|U:{self._url}{'/'+endpoint if endpoint else ''}]" +
                f"[/bold {color}]: {msg}"
            )
        # Now, define the _log dictionary
        self._log = {
            'INFO': partial(_print, "cyan", "INFO"),
            'DEBUG': partial(_print, "yellow", "DEBUG"),
            'ERROR': partial(_print, "red", "ERROR"),
            'SUCCESS': partial(_print, "green", "SUCCESS")
        }

    def info(self, message: str, endpoint: str = "") -> None:
        """Method to print a log as `INFO`

        Args:
            message (str): Message to print,
            endpoint (str | Optional): The endpoint where this log has been sent.
        """
        self._log["INFO"](message, endpoint)

    def debug(self, message: str, endpoint: str = "") -> None:
        """Method to print a log as `DEBUG`

        Args:
            message (str): Message to print,
            endpoint (str | Optional): The endpoint where this log has been sent.
        """
        self._log["DEBUG"](message, endpoint)

    def error(self, message: str, endpoint: str = "") -> None:
        """Method to print a log as `ERROR`

        Args:
            message (str): Message to print,
            endpoint (str | Optional): The endpoint where this log has been sent.
        """
        self._log["ERROR"](message, endpoint)

    def success(self, message: str, endpoint: str = "") -> None:
        """Method to print a log as `SUCCESS`

        Args:
            message (str): Message to print,
            endpoint (str | Optional): The endpoint where this log has been sent.
        """
        self._log["SUCCESS"](message, endpoint)

    def set_url(self, url: str) -> None:
        """Set the URL to be displayed in the log

        Args:
            url (str): URL to display
        """
        self._url = url
