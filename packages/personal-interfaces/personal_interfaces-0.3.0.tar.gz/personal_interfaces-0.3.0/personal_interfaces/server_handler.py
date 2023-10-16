"""
File that runs the app
either for local servers or for deploys.
"""
# Now, import the App
from typing import Generator, Callable, Any
import os
import asyncio
import contextlib
import time
import threading
import argparse
import uvicorn
# Local imports
from .logger import Logger

# Instance the logger as general
logger = Logger()


class Server:
    """Class object to setup the Server as a secondary process so the main thread can
    run without being blocked. The main arguments are:
    Args:
        host (str | Optional): The host to connect to. Default to "localhost".
        port (int | Optional): The port to connect to. Default to 3000.
        log_level (str | Optional): The type of log output. Default to "debug".
    """

    def __init__(self,  # pylint: disable=R0913
                 app: Any,
                 host: str = os.environ.get("HOST", "0.0.0.0"),
                 port: str = os.environ.get("PORT", "3000"),
                 log_level: str = "critical",
                 reload: bool = False
                 ) -> None:
        super().__init__()
        self.app = app()
        # Now, define the configuration for uvicorn
        self.config = uvicorn.Config(app=self.app.client,
                                     host=host,
                                     port=int(port),
                                     log_level=log_level,
                                     reload=reload,
                                     reload_dirs="server/app")
        self.server = CustomServer(self.config)

    def run(self) -> Callable:
        """Method to run the server using the run_in_thread method of the CustomServer."""
        logger.success("Server deployed successfully...")
        return self.server.run_in_thread()

    def close(self) -> None:
        """Method to close the server."""
        logger.success('Closing server...')


class CustomServer(uvicorn.Server):  # pylint: disable=R0903
    """Custom uvicorn.Server class that uses threading to manage the connection."""
    # Define the variable here as it was a __init__
    should_exit = False

    @contextlib.contextmanager
    def run_in_thread(self) -> Generator:
        """Method to run in a secondary thread to not stop the other processes."""
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


async def keep_running() -> None:
    """Function to keep running the server..."""
    while True:
        await asyncio.sleep(30)
        logger.debug("Server alive...")


def run_server(
    api_to_run: Any,
    host: str = "0.0.0.0",
    port: str = "3000",
    **kwargs
) -> None:
    """Function to deploy the server."""
    # Set the URL to the logger
    logger.set_url(f"https://{host}{':' if port else ''}{port}")
    if kwargs:
        logger.info("Arguments...")
        for k_arg, v_arg in kwargs.items():
            logger.log(f"{k_arg}: {v_arg}")
    logger.info(48*'-')
    # First, obtain the port that we're trying to connect
    # Add the default port value, just in case
    _port = os.environ.get("PORT", port)
    # Now, argparse the host
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default=host)
    parser.add_argument("--port", type=int, default=_port)
    parser.add_argument("--log", type=str, default='critical')
    parser.add_argument("--r", type=bool, default=True)
    _args, _ = parser.parse_known_args()

    # ---------------------------------------------------------------- #
    #                       RUN THE SERVER                             #
    # ---------------------------------------------------------------- #
    server = Server(
        app=api_to_run,
        host=_args.host,
        port=_port,
        log_level=_args.log,
        reload=_args.r
    )
    with server.run():  # type: ignore
        # Start the loop event
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # Begin the try-catch block
        try:
            # Now, ensure the run forever part
            asyncio.ensure_future(keep_running())
            loop.run_forever()
        # Only close this with a keyboardInterrupt (for local tests)
        except KeyboardInterrupt:
            loop.close()  # Close the loop
            server.close()
