import logging
import os
import sys
from datetime import datetime
from functools import wraps
from importlib import metadata
from pathlib import Path
from platform import platform
from traceback import extract_tb
from typing import Callable

from rich.console import Console
from rich.logging import RichHandler

from .check_PyPI_version import check_version_on_console_thread
from .py_utils import IdtrackeraiError, resolve_path

LOG_FILE_PATH = resolve_path("idtrackerai.log")

ERROR_MSG = (
    "\n\nIf this error persists please let us know by "
    "following any of the following options:\n"
    "  - Posting on "
    "https://groups.google.com/g/idtrackerai_users\n"
    "  - Opening an issue at "
    "https://gitlab.com/polavieja_lab/idtrackerai\n"
    "  - Sending an email to idtrackerai@gmail.com\n"
    f"Share the log file ({LOG_FILE_PATH}) when "
    "doing any of the options above"
)


def initLogger(level: int = logging.DEBUG):
    logger_width_when_no_terminal = 130
    try:
        os.get_terminal_size()
    except OSError:
        # stdout is sent to file. We define logger width to a constant
        size = logger_width_when_no_terminal
    else:
        # stdout is sent to terminal
        # We define logger width to adapt to the terminal width
        size = None

    LOG_FILE_PATH.unlink(True)  # avoid conflicts and merged files

    # The first handler is the terminal, the second one the .log file,
    # both rendered with Rich and full logging (level=0)
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="%H:%M:%S",
        force=True,
        handlers=[
            RichHandler(console=Console(width=size), rich_tracebacks=True),
            RichHandler(
                console=Console(
                    file=LOG_FILE_PATH.open("w", encoding="utf_8"),  # noqa SIM115
                    width=logger_width_when_no_terminal,
                )
            ),
        ],
    )

    logging.captureWarnings(True)
    logging.info("[bright_white]Welcome to idtracker.ai", extra={"markup": True})
    logging.debug(
        f"Running idtracker.ai '{metadata.version('idtrackerai')}'"
        f" on Python '{sys.version.split(' ')[0]}'\nPlatform: '{platform(True)}'"
        "\nDate: "
        + str(datetime.now()).split(".")[0]
    )
    logging.info("Writing log in %s", LOG_FILE_PATH)


def wrap_entrypoint(main_function: Callable):
    @wraps(main_function)
    def ret_fun(*args, **kwargs):
        initLogger()
        check_version_on_console_thread()
        try:
            return main_function(*args, **kwargs)
        except IdtrackeraiError as error:
            tb = extract_tb(error.__traceback__)[-1]
            logging.critical(
                "%s [bright_black](from %s:%d)[/]",
                error,
                Path(*Path(tb.filename).parts[-2:]),
                tb.lineno,
                extra={"markup": True},
            )
            return False
        except KeyboardInterrupt:
            logging.critical("KeyboardInterrupt", exc_info=False)
            return False
        except ModuleNotFoundError as error:
            if "torch" in str(error):
                logging.critical(
                    "Module PyTorch is not installed, follow their guideline to install"
                    " it (https://pytorch.org/get-started/locally/). Original"
                    ' exception: "%s"',
                    error,
                )
                return False
            logging.critical("%s: %s", type(error).__name__, error, exc_info=error)
            logging.info(ERROR_MSG)
            return False
        except Exception as error:
            logging.critical("%s: %s", type(error).__name__, error, exc_info=error)
            logging.info(ERROR_MSG)
            return False

    return ret_fun
