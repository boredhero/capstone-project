import logging, logging.config
import os, traceback
from typing import Any

from misc import Singleton, get_human_readable_time_with_timezone, get_unix_timestamp

class GameLogger(metaclass=Singleton):

    def __init__(self):
        """
        Freedom gateway Logger
        Log shit, to ALL the places at once!
        """
        try:
            self.__start_logged = False
            self.__start_time = get_unix_timestamp()
            self.__start_time_human_readable = get_human_readable_time_with_timezone(unix_timestamp=self.__start_time)
            self.__log_folder = "logs"
            logging.basicConfig(
                level=logging.INFO,  # Set the desired logging level (e.g., INFO, DEBUG, ERROR)
                format="%(asctime)s [%(levelname)s]: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                handlers=[
                    logging.FileHandler(os.path.join(self.__log_folder, f"{self.__start_time_human_readable}.log")),
                    logging.StreamHandler(),  # Log to the console
                ]
            )
            self.__logger = logging.getLogger()
            self.info("Successful Init GameLogger", name=__name__)

        except Exception:
            print(f"[GameLogger Error] Error initializing GameLogger! :: \n{traceback.format_exc()}")

    def __log(self, level: str, msg: str, name: str | None = None, print_formatting: bool = True, exception: Exception | None = None):
        try:
            err = ""
            if exception is not None:
                err = self.__format_exception(exception)
                err = f"\n{err}"
            msg = str(msg)
            ts = get_human_readable_time_with_timezone(now=True)
            match level:
                case "CRITICAL":
                    log_str = f"[{name}][{level}] :: {msg}{err}"
                    self.__logger.critical(log_str)
                case "ERROR":
                    log_str = f"[{name}][{level}] :: {msg}{err}"
                    self.__logger.error(log_str)
                case "WARNING":
                    log_str = f"[{name}][{level}] :: {msg}{err}"
                    self.__logger.warning(log_str)
                case "DEBUG":
                    log_str = f"[{name}][{level}] :: {msg}{err}"
                    self.__logger.debug(log_str)
                case _:
                    log_str = f"[{name}][{level}] :: {msg}{err}"
                    self.__logger.info(log_str)
            if name is None:
                name = "FGLogger"
            if print_formatting is True:
                print(f"[{ts}][{name}][{level}] :: {msg}{err}")
            else:
                print(msg)
        except Exception:
            print(f"[GameLogger Error] Error logging message: {msg}")
            print(traceback.format_exc())

    def __format_exception(self, ex: Exception) -> str:
        """Returns a string (formatted with newlines) for logging exceptions!"""
        try:
            lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
            text = ''.join(lines)
            return text
        except Exception as e:
            print(f"[GameLogger Error] Error formatting exception: {ex}")
            self.error("An unknown error occurred while formatting an exception!", name=__name__, exception=e) # This should be fine because we know e will be valid here!
            return ""

    def critical(self, msg: str, name: str | None = None, print_formatting: bool = True, exception: Exception | None = None):
        """GameLogger Level CRITICAL"""
        try:
            self.__log("CRITICAL", msg, name=name, print_formatting=print_formatting, exception=exception)
        except Exception:
            print("Caught exception in CRITICAL")

    def error(self, msg: str, name: str | None = None, print_formatting: bool = True, exception: Exception | None = None):
        """GameLogger Level ERROR"""
        try:
            self.__log("ERROR", msg, name=name, print_formatting=print_formatting, exception=exception)
        except Exception:
            print("Caught exception in ERROR")

    def warning(self, msg: str, name: str | None = None, print_formatting: bool = True, exception: Exception | None = None):
        """GameLogger Level WARNING"""
        try:
            self.__log("WARNING", msg, name=name, print_formatting=print_formatting, exception=exception)
        except Exception:
            print("Caught exception in WARNING")

    def info(self, msg: str, name: str | None = None, print_formatting: bool = True, exception: Exception | None = None):
        """GameLogger Level INFO"""
        try:
            self.__log("INFO", msg, name=name, print_formatting=print_formatting, exception=exception)
        except Exception:
            print("Caught exception in INFO")

    def debug(self, msg: str, name: str | None = None, print_formatting: bool = True, exception: Exception | None = None):
        """GameLogger Level DEBUG"""
        try:
            self.__log("DEBUG", msg, name=name, print_formatting=print_formatting, exception=exception)
        except Exception:
            print("Caught exception in DEBUG")

    def log_startup(self, version: Any, title: Any):
        """
        Print the startup message and log it
        """
        if self.__start_logged is False:
            self.__logger.info("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
            self.__logger.info(str(f"Starting {title} v{version}"))
            self.__logger.info("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
            self.__start_logged = True
