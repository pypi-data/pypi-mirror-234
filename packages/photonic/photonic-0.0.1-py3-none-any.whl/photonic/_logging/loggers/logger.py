# Built-in Libs
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from threading import Lock

# Custom Libs
from src.photonic.utils.threading_utils import threaded


class Logger:
    def __init__(self, logger_name, level=DEBUG):
        self.__logger = getLogger(logger_name)
        self.__logger.setLevel(level)

        self.__file_lock = Lock()

    def debug(self, message: str) -> None:
        self.__log(DEBUG, message)

    def info(self, message: str) -> None:
        self.__log(INFO, message)

    def warning(self, message: str) -> None:
        self.__log(WARNING, message)

    def error(self, message: str) -> None:
        self.__log(ERROR, message)

    def critical(self, message: str) -> None:
        self.__log(CRITICAL, message)

    @threaded
    def __log(self, level, message: str) -> None:
        with self.__file_lock:
            self.__logger.log(level, message)  # Check stacklevel argument
