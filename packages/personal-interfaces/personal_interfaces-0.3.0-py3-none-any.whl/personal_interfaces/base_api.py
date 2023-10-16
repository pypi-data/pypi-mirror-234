"""
Provide a Base API to use on the server handler
"""
import attr
from fastapi import FastAPI
# Import also the CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware


@attr.s(slots=True)
class BaseAPI():  # pylint: disable=R0903
    """Base class of a WebAPI. Include:

    - client (property): To return the client and be used in the `run_server`
    - allow_cors_middleware: To config a pre-determinate middleware
    """
    _app: FastAPI = attr.ib(default=None)

    def allow_cors_middleware(self) -> None:
        """Allow the cors middleware config"""
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

    @property
    def client(self) -> FastAPI:
        """Method that only returns the FastAPI object

        Returns:
            FastAPI: FastAPI object
        """
        return self._app
