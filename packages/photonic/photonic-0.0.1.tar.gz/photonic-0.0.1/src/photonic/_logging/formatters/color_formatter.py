from logging import Formatter, LogRecord

from src.photonic.enums.colors import AnsiColor


class ColorFormatter(Formatter):
    color_map = {
        "DEBUG": AnsiColor.GREY,
        "INFO": AnsiColor.BLUE,
        "WARNING": AnsiColor.YELLOW,
        "ERROR": AnsiColor.RED,
        "CRITICAL": AnsiColor.BOLD_RED
    }

    def format(self, record: LogRecord) -> str:
        log = super().format(record)
        colored_log = ColorFormatter.color_map[record.levelname].value + log + AnsiColor.RESET.value

        return colored_log
