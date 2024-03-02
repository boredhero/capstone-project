import logging, logging.config
import os, traceback
from typing import Any

import appdirs

from misc import Singleton, get_human_readable_time_with_timezone, get_unix_timestamp

class GameLogger(metaclass=Singleton):

    def __init__(self):
        """
        Game Logger
        """
        try:
            self.__start_logged = False
            self.__start_time = get_unix_timestamp()
            self.__start_time_human_readable = get_human_readable_time_with_timezone(unix_timestamp=self.__start_time)
            self.__log_folder = "logs"
            self.__log_folder = appdirs.user_log_dir(appname="Instance", appauthor="boredhero")
            os.makedirs(self.__log_folder, exist_ok=True)
            self.__log_file_path = os.path.join(self.__log_folder, f"{self.__start_time_human_readable}.log")
            logging.basicConfig(
                level=logging.DEBUG,
                format="[%(asctime)s][%(levelname)s]%(message)s",
                datefmt="%Y-%m-%d_%H:%M:%S",
                handlers=[
                    logging.FileHandler(self.__log_file_path),
                    logging.StreamHandler(),  # Log to the console
                ]
            )
            self.__logger = logging.getLogger()
            self.info("Successful Init GameLogger", name=__name__)
            self.__clear_log_folder()
        except Exception:
            print(f"[GameLogger Error] Error initializing GameLogger! :: \n{traceback.format_exc()}")

    def __log(self, level: str, msg: str, name: str | None = None, exception: Exception | None = None):
        try:
            err = ""
            if exception is not None:
                err = self.__format_exception(exception)
                err = f"\n{err}"
            msg = str(msg)
            match level:
                case "CRIT":
                    log_str = f"[{name}] :: {msg}{err}"
                    self.__logger.critical(log_str)
                case "ERROR":
                    log_str = f"[{name}] :: {msg}{err}"
                    self.__logger.error(log_str)
                case "WARN":
                    log_str = f"[{name}] :: {msg}{err}"
                    self.__logger.warning(log_str)
                case "DEBUG":
                    log_str = f"[{name}] :: {msg}{err}"
                    self.__logger.debug(log_str)
                case _:
                    log_str = f"[{name}] :: {msg}{err}"
                    self.__logger.info(log_str)
            if name is None:
                name = "GLogger"
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

    def __clear_log_folder(self):
        """
        Deletes all files in the log folder
        """
        try:
            for file in os.listdir(self.__log_folder):
                file_path = os.path.join(self.__log_folder, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            self.info("Successful Delete All Previous Log Files", name=__name__)
        except Exception as e:
            print(f"[GameLogger Error] Error clearing log files: {e}")
            self.error("Error occurred while clearing log files", name=__name__, exception=e)

    def critical(self, msg: str, name: str | None = None, exception: Exception | None = None):
        """GameLogger Level CRITICAL"""
        try:
            self.__log("CRIT", msg, name=name, exception=exception)
        except Exception:
            print("Caught exception in CRITICAL")

    def error(self, msg: str, name: str | None = None, exception: Exception | None = None):
        """GameLogger Level ERROR"""
        try:
            self.__log("ERROR", msg, name=name, exception=exception)
        except Exception:
            print("Caught exception in ERROR")

    def warning(self, msg: str, name: str | None = None, exception: Exception | None = None):
        """GameLogger Level WARNING"""
        try:
            self.__log("WARN", msg, name=name, exception=exception)
        except Exception:
            print("Caught exception in WARNING")

    def info(self, msg: str, name: str | None = None, exception: Exception | None = None):
        """GameLogger Level INFO"""
        try:
            self.__log("INFO", msg, name=name, exception=exception)
        except Exception:
            print("Caught exception in INFO")

    def debug(self, msg: str, name: str | None = None, exception: Exception | None = None):
        """GameLogger Level DEBUG"""
        try:
            self.__log("DEBUG", msg, name=name, exception=exception)
        except Exception:
            print("Caught exception in DEBUG")

    def log_startup(self, version: Any, title: Any):
        """
        Print the startup message and log it
        """
        if self.__start_logged is False:
            self.__logger.info("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
            self.__logger.info(str(f" Starting {title} v{version}"))
            self.__logger.info("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
            self.__start_logged = True
