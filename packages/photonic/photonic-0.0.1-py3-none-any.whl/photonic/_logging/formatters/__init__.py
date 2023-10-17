from enum import Enum

from .color_formatter import ColorFormatter


class Format(Enum):
    date_format = "%Y-%m-%d %H:%M:%S"
    brief_format = "%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s"
    detailed_format = (
        """{
        Level: %(levelname)s,
        File: %(filename)s,
        Function: %(funcName)s,
        Line: %(lineno)d,
        Time: %(asctime)s,
        Message: %(message)s
    }"""
    )
    detailed_json_format = (
        """
        {
            "Level": "%(levelname)s",
            "File": "%(filename)s",
            "Function": "%(funcName)s",
            "Line": "%(lineno)d",
            "Time": "%(asctime)s",
            "Message": "%(message)s"
        }
        """
    )
