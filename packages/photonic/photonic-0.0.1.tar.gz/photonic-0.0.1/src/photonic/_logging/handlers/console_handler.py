from logging import StreamHandler, WARNING, Formatter
from sys import stdout

from src.photonic._logging.formatters import Format


class ConsoleHandler(StreamHandler):
    def __init__(self, level=WARNING, formatter=Formatter(Format.brief_format.value, Format.date_format.value)):
        super().__init__(stream=stdout)
        self.setLevel(level)
        self.setFormatter(formatter)
